from rest_framework.status import HTTP_400_BAD_REQUEST

ERROR_INTEGRATION_AUTHORIZED_USER_INVALID = (
    "ERROR_INTEGRATION_AUTHORIZED_USER_INVALID",
    HTTP_400_BAD_REQUEST,
    "The specified authorizer user cannot be used as they either don't "
    "belong to the integration's workspace, or are flagged for deletion.",
)
