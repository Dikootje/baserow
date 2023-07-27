from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

ERROR_BUILDER_DOES_NOT_EXIST = (
    "ERROR_BUILDER_DOES_NOT_EXIST",
    HTTP_404_NOT_FOUND,
    "The builder for the requested domain does not exist.",
)
ERROR_INTEGRATION_AUTHORIZED_USER_INVALID = (
    "ERROR_INTEGRATION_AUTHORIZED_USER_INVALID",
    HTTP_400_BAD_REQUEST,
    "The specified authorizer user cannot be used as they either don't "
    "belong to the integration's workspace, or are flagged for deletion.",
)
