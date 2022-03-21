class DumbException(Exception):
    pass


class DumbValueError(ValueError, DumbException):
    pass
