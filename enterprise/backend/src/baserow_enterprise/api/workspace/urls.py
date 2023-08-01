from django.urls import include, re_path

from .audit_log import urls as audit_log_urls

app_name = "baserow_enterprise.api.workspace"

urlpatterns = [
    re_path(
        r"(?P<workspace_id>[0-9]+)/audit-log/",
        include(audit_log_urls, namespace="audit_log"),
    ),
]
