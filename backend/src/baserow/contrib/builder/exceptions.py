class BuilderDoesNotExist(Exception):
    """Raised when trying to get a domain that doesn't exist."""


class InvalidIntegrationAuthorizedUser(Exception):
    """Raised when an integration is created or updated with an authorized_user
    that is either not in the integration's workspace, or flagged for deletion."""
