import string

import deal

deal.activate()
deal.module_load(deal.pure)

MIN_PASSWORD_LENGTH = 5
MAX_PASSWORD_LENGTH = 64

DEFAULT_DIGITS = string.digits
DEFAULT_EXTRAS = string.punctuation
DEFAULT_LOWERS = string.ascii_lowercase
DEFAULT_UPPERS = string.ascii_uppercase
DEFAULT_BLOCKS = """'";"""
