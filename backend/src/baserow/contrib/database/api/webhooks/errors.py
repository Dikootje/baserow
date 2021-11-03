from django.conf import settings

from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

ERROR_TABLE_WEBHOOK_DOES_NOT_EXIST = (
    "ERROR_TABLE_WEBHOOK_DOES_NOT_EXIST",
    HTTP_404_NOT_FOUND,
    "The requested table webhook does not exist.",
)

ERROR_TABLE_WEBHOOK_MAX_LIMIT_EXCEEDED = (
    "ERROR_TABLE_WEBHOOK_MAX_LIMIT_EXCEEDED",
    HTTP_400_BAD_REQUEST,
    f"The maximally allowed webhooks per table has been exceeded. You can provide "
    f"a maximum of {settings.WEBHOOKS_MAX_PER_TABLE} webhooks.",
)

ERROR_TABLE_WEBHOOK_CANNOT_BE_CALLED = (
    "ERROR_TABLE_WEBHOOK_CANNOT_BE_CALLED",
    HTTP_400_BAD_REQUEST,
    "The table webhook cannot be called.",
)

ERROR_TABLE_WEBHOOK_ALREADY_EXISTS = (
    "ERROR_TABLE_WEBHOOK_ALREADY_EXISTS",
    HTTP_400_BAD_REQUEST,
    "A table webhook with the given url and request method already exists.",
)
