from django.db import transaction
from django.utils import translation

from baserow_premium.api.admin.views import AdminListingView
from baserow_premium.license.handler import LicenseHandler
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_202_ACCEPTED
from rest_framework.views import APIView

from baserow.api.decorators import (
    map_exceptions,
    validate_body,
    validate_query_parameters,
)
from baserow.api.jobs.errors import ERROR_MAX_JOB_COUNT_EXCEEDED
from baserow.api.jobs.serializers import JobSerializer
from baserow.api.schemas import CLIENT_SESSION_ID_SCHEMA_PARAMETER, get_error_schema
from baserow.core.jobs.exceptions import MaxJobCountExceeded
from baserow.core.jobs.handler import JobHandler
from baserow.core.jobs.registries import job_type_registry
from baserow.core.models import User, Workspace
from baserow_enterprise.api.workspace.audit_log.serializers import (
    serialize_filtered_action_types,
)
from baserow_enterprise.audit_log.job_types import AuditLogExportJobType
from baserow_enterprise.audit_log.models import AuditLogEntry
from baserow_enterprise.features import AUDIT_LOG

from .serializers import (
    AdminAuditLogQueryParamsSerializer,
    AdminAuditLogSerializer,
    AuditLogActionTypeSerializer,
    AuditLogExportJobRequestSerializer,
    AuditLogExportJobResponseSerializer,
    AuditLogUserSerializer,
    AuditLogWorkspaceSerializer,
)


class AdminAuditLogView(AdminListingView):
    permission_classes = (IsAdminUser,)
    serializer_class = AdminAuditLogSerializer
    filters_field_mapping = {
        "user_id": "user_id",
        "workspace_id": "workspace_id",
        "action_type": "action_type",
        "from_timestamp": "action_timestamp__gte",
        "to_timestamp": "action_timestamp__lte",
        "ip_address": "ip_address",
    }
    sort_field_mapping = {
        "user": "user_email",
        "workspace": "workspace_name",
        "type": "action_type",
        "timestamp": "action_timestamp",
        "ip_address": "ip_address",
    }
    default_order_by = "-action_timestamp"

    def get_queryset(self, request):
        return AuditLogEntry.objects.all()

    def get_serializer(self, request, *args, **kwargs):
        return super().get_serializer(
            request, *args, context={"request": request}, **kwargs
        )

    @extend_schema(
        tags=["Admin"],
        operation_id="admin_list_audit_log_entries",
        description="Lists all audit log entries.\n\nThis is a **enterprise** feature.",
        **AdminListingView.get_extend_schema_parameters(
            "audit log entries",
            serializer_class,
            [],
            sort_field_mapping,
            extra_parameters=[
                OpenApiParameter(
                    name="user_id",
                    location=OpenApiParameter.QUERY,
                    type=OpenApiTypes.INT,
                    description="Filter the audit log entries by user id.",
                ),
                OpenApiParameter(
                    name="workspace_id",
                    location=OpenApiParameter.QUERY,
                    type=OpenApiTypes.INT,
                    description="Filter the audit log entries by workspace id.",
                ),
                OpenApiParameter(
                    name="action_type",
                    location=OpenApiParameter.QUERY,
                    type=OpenApiTypes.STR,
                    description="Filter the audit log entries by action type.",
                ),
                OpenApiParameter(
                    name="from_timestamp",
                    location=OpenApiParameter.QUERY,
                    type=OpenApiTypes.STR,
                    description="The ISO timestamp to filter the audit log entries from.",
                ),
                OpenApiParameter(
                    name="to_timestamp",
                    location=OpenApiParameter.QUERY,
                    type=OpenApiTypes.STR,
                    description="The ISO timestamp to filter the audit log entries to.",
                ),
            ],
        ),
    )
    @validate_query_parameters(AdminAuditLogQueryParamsSerializer)
    def get(self, request, query_params):
        LicenseHandler.raise_if_user_doesnt_have_feature_instance_wide(
            AUDIT_LOG, request.user
        )
        with translation.override(request.user.profile.language):
            return super().get(request)


class AdminAuditLogUserFilterView(AdminListingView):
    permission_classes = (IsAdminUser,)
    serializer_class = AuditLogUserSerializer
    search_fields = ["email"]
    default_order_by = "email"

    def get_queryset(self, request):
        return User.objects.all()

    @extend_schema(
        tags=["Admin"],
        operation_id="admin_list_audit_log_users",
        description=(
            "List all users that have performed an action in the audit log."
            "\n\nThis is a **enterprise** feature."
        ),
        **AdminListingView.get_extend_schema_parameters(
            "users", serializer_class, search_fields, {}
        ),
    )
    def get(self, request):
        LicenseHandler.raise_if_user_doesnt_have_feature_instance_wide(
            AUDIT_LOG, request.user
        )
        return super().get(request)


class AdminAuditLogWorkspaceFilterView(AdminListingView):
    permission_classes = (IsAdminUser,)
    serializer_class = AuditLogWorkspaceSerializer
    search_fields = ["name"]
    default_order_by = "name"

    def get_queryset(self, request):
        return Workspace.objects.filter(template__isnull=True)

    @extend_schema(
        tags=["Admin"],
        operation_id="admin_list_audit_log_workspaces",
        description=(
            "List all distinct workspace names related to an audit log entry."
            "\n\nThis is a **enterprise** feature."
        ),
        **AdminListingView.get_extend_schema_parameters(
            "workspaces", serializer_class, search_fields, {}
        ),
    )
    def get(self, request):
        LicenseHandler.raise_if_user_doesnt_have_feature_instance_wide(
            AUDIT_LOG, request.user
        )
        return super().get(request)


class AdminAuditLogActionTypeFilterView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = AuditLogActionTypeSerializer

    @extend_schema(
        tags=["Admin"],
        operation_id="admin_list_audit_log_action_types",
        description=(
            "List all distinct action types related to an audit log entry."
            "\n\nThis is a **enterprise** feature."
        ),
        parameters=[
            OpenApiParameter(
                name="search",
                location=OpenApiParameter.QUERY,
                type=OpenApiTypes.STR,
                description="If provided only action_types with name "
                "that match the query will be returned.",
            )
        ],
        responses={
            200: serializer_class(many=True),
            400: get_error_schema(
                [
                    "ERROR_PAGE_SIZE_LIMIT",
                    "ERROR_INVALID_PAGE",
                    "ERROR_INVALID_SORT_DIRECTION",
                    "ERROR_INVALID_SORT_ATTRIBUTE",
                ]
            ),
            401: None,
        },
    )
    def get(self, request):
        LicenseHandler.raise_if_user_doesnt_have_feature_instance_wide(
            AUDIT_LOG, request.user
        )
        search = request.GET.get("search", None)
        return Response(serialize_filtered_action_types(request.user, search))


class AsyncAdminAuditLogExportView(APIView):
    permission_classes = (IsAdminUser,)

    @extend_schema(
        parameters=[CLIENT_SESSION_ID_SCHEMA_PARAMETER],
        tags=["Admin"],
        operation_id="admin_async_export_audit_log_entries",
        description=(
            "Creates a job to export the filtered audit log to a CSV file from the Admin section."
            "\n\nThis is a **enterprise** feature."
        ),
        request=AuditLogExportJobRequestSerializer,
        responses={
            202: AuditLogExportJobResponseSerializer,
            400: get_error_schema(
                ["ERROR_REQUEST_BODY_VALIDATION", "ERROR_MAX_JOB_COUNT_EXCEEDED"]
            ),
        },
    )
    @transaction.atomic
    @map_exceptions({MaxJobCountExceeded: ERROR_MAX_JOB_COUNT_EXCEEDED})
    @validate_body(AuditLogExportJobRequestSerializer)
    def post(self, request, data):
        """Creates a job to export the filtered audit log entries to a CSV file."""

        LicenseHandler.raise_if_user_doesnt_have_feature_instance_wide(
            AUDIT_LOG, request.user
        )

        csv_export_job = JobHandler().create_and_start_job(
            request.user, AuditLogExportJobType.type, **data
        )

        serializer = job_type_registry.get_serializer(
            csv_export_job, JobSerializer, context={"request": request}
        )
        return Response(serializer.data, status=HTTP_202_ACCEPTED)
