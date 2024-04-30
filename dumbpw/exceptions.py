class DumbError(Exception):
    pass


class DumbValueError(ValueError, DumbError):
    pass
