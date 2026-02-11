"""Define exceptions and error states for dumbpw."""


class DumbError(Exception):
    """Generic exception."""


class DumbValueError(ValueError, DumbError):
    """ValueError for own objects."""
