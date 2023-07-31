from typing import Dict, Optional

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from drf_spectacular.utils import extend_schema_serializer
from opentelemetry import metrics
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken

from baserow.api.sessions import set_user_session_data_from_request
from baserow.api.user.jwt import get_user_from_token
from baserow.api.user.registries import user_data_registry
from baserow.api.user.validators import (
    email_notification_frequency,
    language_validation,
    password_validation,
)
from baserow.api.workspaces.invitations.serializers import (
    UserWorkspaceInvitationSerializer,
)
from baserow.core.action.registries import action_type_registry
from baserow.core.auth_provider.exceptions import AuthProviderDisabled
from baserow.core.auth_provider.handler import PasswordProviderHandler
from baserow.core.models import Template
from baserow.core.user.actions import SignInUserActionType
from baserow.core.user.exceptions import DeactivatedUserException
from baserow.core.user.utils import (
    generate_session_tokens_for_user,
    normalize_email_address,
)

User = get_user_model()

meter = metrics.get_meter(__name__)
token_refreshes_counter = meter.create_counter(
    "baserow.token_refreshes",
    unit="1",
    description="The number of token refreshes.",
)


class SubjectUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "email"]
        extra_kwargs = {
            "id": {"read_only": True},
            "username": {"read_only": True},
            "first_name": {"read_only": True},
            "email": {"read_only": True},
        }


class UserSerializer(serializers.ModelSerializer):
    language = serializers.CharField(
        source="profile.language",
        required=False,
        min_length=2,
        max_length=10,
        validators=[language_validation],
        help_text="An ISO 639 language code (with optional variant) "
        "selected by the user. Ex: en-GB.",
    )
    email_notification_frequency = serializers.CharField(
        source="profile.email_notification_frequency",
        required=False,
        validators=[email_notification_frequency],
        help_text="The frequency at which the user wants to receive email notifications.",
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "username",
            "password",
            "is_staff",
            "id",
            "language",
            "email_notification_frequency",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "is_staff": {"read_only": True},
            "id": {"read_only": True},
        }


class PublicUserSerializer(serializers.ModelSerializer):
    """
    Serializer that exposes only fields that can be shared
    about the user for the whole group.
    """

    class Meta:
        model = User
        fields = ("id", "username", "first_name")
        extra_kwargs = {
            "id": {"read_only": True},
        }


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=150)
    email = serializers.EmailField(
        help_text="The email address is also going to be the username."
    )
    password = serializers.CharField(validators=[password_validation])
    language = serializers.CharField(
        required=False,
        default=settings.LANGUAGE_CODE,
        min_length=2,
        max_length=10,
        validators=[language_validation],
        help_text="An ISO 639 language code (with optional variant) "
        "selected by the user. Ex: en-GB.",
    )
    authenticate = serializers.BooleanField(
        required=False,
        default=False,
        help_text="Indicates whether an authentication JWT should be generated and "
        "be included in the response.",
    )
    # GroupDeprecation
    group_invitation_token = serializers.CharField(
        required=False,
        source="workspace_invitation_token",
        help_text="DEPRECATED: Please use `workspace_invitation_token` which "
        "this attribute is being renamed to in 2024.",
    )
    workspace_invitation_token = serializers.CharField(
        required=False,
        help_text="If provided and valid, the user accepts the workspace invitation and "
        "will have access to the workspace after signing up.",
    )
    template_id = serializers.PrimaryKeyRelatedField(
        required=False,
        default=None,
        queryset=Template.objects.all(),
        help_text="The id of the template that must be installed after creating the "
        "account. This only works if the `workspace_invitation_token` param is not "
        "provided.",
    )


class AccountSerializer(serializers.Serializer):
    """
    This serializer must be kept in sync with `UserSerializer`.
    """

    first_name = serializers.CharField(min_length=2, max_length=150)
    language = serializers.CharField(
        source="profile.language",
        required=False,
        min_length=2,
        max_length=10,
        validators=[language_validation],
        help_text="An ISO 639 language code (with optional variant) "
        "selected by the user. Ex: en-GB.",
    )
    email_notification_frequency = serializers.CharField(
        source="profile.email_notification_frequency",
        required=False,
        validators=[email_notification_frequency],
        help_text="The frequency at which the user wants to receive email notifications.",
    )


class SendResetPasswordEmailBodyValidationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        help_text="The email address of the user that has requested a password reset."
    )
    base_url = serializers.URLField(
        help_text="The base URL where the user can reset his password. The reset "
        "token is going to be appended to the base_url (base_url "
        "'/token')."
    )


class ResetPasswordBodyValidationSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(validators=[password_validation])


class ChangePasswordBodyValidationSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[password_validation])


class NormalizedEmailField(serializers.EmailField):
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return normalize_email_address(data)


def get_all_user_data_serialized(
    user: AbstractUser, request: Optional[Request] = None
) -> Dict:
    """
    Update the payload with the additional user data that must be added.
    The `user_data_registry` contains instances that want to add additional
    information to this payload.

    :param user: The user for which the data must be serialized.
    :param request: The request that is used to generate the data.
    :return: A dictionary with the serialized data for the user.
    """

    return {
        "user": UserSerializer(user, context={"request": request}).data,
        **user_data_registry.get_all_user_data(user, request),
    }


@extend_schema_serializer(deprecate_fields=["username"])
class TokenObtainPairWithUserSerializer(TokenObtainPairSerializer):
    email = NormalizedEmailField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = NormalizedEmailField(
            required=False, help_text="Deprecated. Use `email` instead."
        )

    def get_username(self, value):
        return value

    def validate(self, attrs):
        """
        This serializer is only used by the ObtainJSONWebToken view which is only used
        to generate a new token. When that happens we want to update the user's last
        login timestamp.
        """

        # this permits to use "email" as field in the serializer giving us compatibility
        # with the TokenObtainPairSerializer that expects "username" instead.
        if not attrs.get(self.username_field):
            email = attrs.get("email")
            if not email:
                raise serializers.ValidationError({"email": "This field is required."})
            attrs[self.username_field] = email

        super().validate(attrs)

        user = self.user
        password_provider = PasswordProviderHandler.get()
        if not password_provider.enabled and user.is_staff is False:
            raise AuthProviderDisabled()
        if not user.is_active:
            raise DeactivatedUserException()

        data = generate_session_tokens_for_user(user, include_refresh_token=True)
        data.update(**get_all_user_data_serialized(user, self.context["request"]))

        set_user_session_data_from_request(user, self.context["request"])
        action_type_registry.get(SignInUserActionType.type).do(user, password_provider)

        return data


@extend_schema_serializer(exclude_fields=["refresh"], deprecate_fields=["token"])
class TokenRefreshWithUserSerializer(TokenRefreshSerializer):
    refresh_token = serializers.CharField(required=False)
    token = serializers.CharField(
        required=False, help_text="Deprecated. Use `refresh_token` instead."
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["refresh"]

    def validate(self, attrs):
        attrs["refresh"] = attrs.pop("refresh_token", attrs.get("token"))
        super().validate(attrs)

        user = get_user_from_token(attrs["refresh"], RefreshToken)
        data = generate_session_tokens_for_user(user)
        data.update(**get_all_user_data_serialized(user, self.context["request"]))
        token_refreshes_counter.add(1)
        return data


@extend_schema_serializer(deprecate_fields=["token"])
class TokenVerifyWithUserSerializer(TokenVerifySerializer):
    refresh_token = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["token"] = serializers.CharField(
            required=False, help_text="Deprecated. Use `refresh_token` instead."
        )

    def validate(self, attrs):
        refresh_token = attrs["token"] = attrs.pop("refresh_token", attrs.get("token"))
        super().validate(attrs)

        user = get_user_from_token(refresh_token, token_class=RefreshToken)
        return get_all_user_data_serialized(user, self.context["request"])


class DashboardSerializer(serializers.Serializer):
    # GroupDeprecation
    group_invitations = UserWorkspaceInvitationSerializer(
        many=True, source="workspace_invitations"
    )
    workspace_invitations = UserWorkspaceInvitationSerializer(many=True)
