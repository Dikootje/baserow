from django.contrib.auth import get_user_model

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from baserow.core.action.registries import action_type_registry
from baserow.core.jobs.registries import job_type_registry
from baserow.core.models import Workspace
from baserow_enterprise.api.workspace.audit_log.serializers import (
    AuditLogActionTypeSerializer,
    AuditLogBaseSerializer,
    AuditLogQueryParamsSerializer,
    AuditLogUserSerializer,
)
from baserow_enterprise.audit_log.job_types import AuditLogExportJobType
from baserow_enterprise.audit_log.models import AuditLogEntry

User = get_user_model()


def render_user(user_id, user_email):
    return f"{user_email} ({user_id})" if user_id else ""


def render_workspace(workspace_id, workspace_name):
    return f"{workspace_name} ({workspace_id})" if workspace_id else ""


def render_action_type(action_type):
    return action_type_registry.get(action_type).get_short_description()


class AdminAuditLogSerializer(AuditLogBaseSerializer, serializers.ModelSerializer):
    group = serializers.SerializerMethodField()  # GroupDeprecation
    workspace = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.STR)
    def get_group(self, instance):  # GroupDeprecation
        return self.get_workspace(instance)

    @extend_schema_field(OpenApiTypes.STR)
    def get_workspace(self, instance):
        return render_workspace(instance.workspace_id, instance.workspace_name)

    class Meta:
        model = AuditLogEntry
        fields = (
            "id",
            "action_type",
            "user",
            "group",  # GroupDeprecation
            "workspace",
            "type",
            "description",
            "timestamp",
            "ip_address",
        )
        read_only_fields = fields


class AuditLogWorkspaceSerializer(serializers.ModelSerializer):
    value = serializers.CharField(source="name")

    class Meta:
        model = Workspace
        fields = ("id", "value")


AuditLogExportJobRequestSerializer = job_type_registry.get(
    AuditLogExportJobType.type
).get_serializer_class(
    base_class=serializers.Serializer,
    request_serializer=True,
    meta_ref_name="SingleAuditLogExportJobRequestSerializer",
)

AuditLogExportJobResponseSerializer = job_type_registry.get(
    AuditLogExportJobType.type
).get_serializer_class(
    base_class=serializers.Serializer,
    meta_ref_name="SingleAuditLogExportJobResponseSerializer",
)


class AdminAuditLogQueryParamsSerializer(AuditLogQueryParamsSerializer):
    workspace_id = serializers.IntegerField(min_value=0, required=False, default=None)


__all__ = [
    "AdminAuditLogSerializer",
    "AuditLogUserSerializer",
    "AuditLogWorkspaceSerializer",
    "AuditLogActionTypeSerializer",
    "AuditLogExportJobRequestSerializer",
    "AuditLogExportJobResponseSerializer",
    "AdminAuditLogQueryParamsSerializer",
]
