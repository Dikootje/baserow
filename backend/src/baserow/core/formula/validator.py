from typing import Any

from django.core.exceptions import ValidationError


def ensure_integer(value: Any) -> int:
    """
    Ensures that the value is an integer or can be converted to an integer.
    Raises a ValidationError if the value is not a valid integer or convertible to an
    integer.

    :param value: The value to ensure as an integer.
    :return: The value as an integer if conversion is successful.
    :raises ValidationError: If the value is not a valid integer or convertible to an
        integer.
    """

    try:
        return int(value)
    except (ValueError, TypeError):
        raise ValidationError(
            "The value must be an integer or convertible to an integer."
        )


def ensure_string(value: Any) -> str:
    """
    Ensures that the value is a string or convert it if not.

    :param value: The value to ensure as a string.
    :return: The value as a string.
    :raises ValidationError: If the value is not a valid str or convertible to a
        str.
    """

    if value is None:
        return ""

    try:
        return str(value)
    except (ValueError, TypeError):
        raise ValidationError("The value must be a string or convertible to a string.")
