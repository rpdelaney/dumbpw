import string

import deal

deal.activate()
deal.module_load(deal.pure)

PASSWORD_LENGTH_MIN = 5
PASSWORD_LENGTH_MAX = 64

DEFAULT_DIGITS = string.digits
DEFAULT_EXTRAS = string.punctuation
DEFAULT_LOWERS = string.ascii_lowercase
DEFAULT_UPPERS = string.ascii_uppercase
DEFAULT_BLOCKS = """'";"""
