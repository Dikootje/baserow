class BuilderDoesNotExist(Exception):
    """Raised when trying to get a domain that doesn't exist."""


class InvalidIntegrationAuthorizedUser(Exception):
    """Raised when an integration authorized user is chosen who doesn't fit our
    criteria, usually because they're not in the workspace or marked for deletion."""
