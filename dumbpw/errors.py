"""Define exceptions and error states for dumbpw."""

import os
from enum import IntEnum


class DumbError(Exception):
    """Generic exception."""


class DumbValueError(ValueError, DumbError):
    """ValueError for own objects."""


class DumbExitCode(IntEnum):
    """Exit status codes corresponding to 'sysexits.h'."""

    CONFIG = os.EX_CONFIG
    DATA_ERR = os.EX_DATAERR
    IO_ERR = os.EX_IOERR
    NO_INPUT = os.EX_NOINPUT
    OK = os.EX_OK
    SOFTWARE = os.EX_SOFTWARE
    USAGE = 2
