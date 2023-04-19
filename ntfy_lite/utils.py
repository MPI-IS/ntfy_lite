"""
Module defining the function 'validate_url'.
"""
import typing
import validators


def validate_url(attribute: str, value: typing.Optional[str]) -> None:
    """
    Return None if value is a valid URL or is None,
    raises a ValueError otherwise.

    Args:
      attribute: an arbitrary string, used in the message of the
        raised ValueError
      value: the string to check
    """
    if value is None:
        return
    if validators.url(value) is not True:
        raise ValueError(f"the value for {attribute} ({value}) is not an url")
    return
