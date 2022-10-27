class TeamDoesNotExist(Exception):
    """Raised when trying to get a team that does not exist."""


class TeamNameNotUnique(Exception):
    """Raised when trying to create/update a team and the name is in use in the group."""


class TeamSubjectDoesNotExist(Exception):
    """Raised when trying to get a subject that does not exist."""


class TeamSubjectTypeUnsupported(Exception):
    """Raised when a subject is invited to a team, and we don't support its type."""


class TeamSubjectBadRequest(Exception):
    """Raised when a subject is created with no ID or email address."""
