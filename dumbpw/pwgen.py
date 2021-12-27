import secrets

import deal

from .candidate import Candidate
from .charspace import Charspace


@deal.pre(
    validator=lambda _: _.min_uppercase
    + _.min_lowercase
    + _.min_digits
    + _.min_specials
    < _.min_length,
    exception=ValueError,
    message="You cannot request more characters than the password length.",
)
def search(
    min_length: int,
    min_uppercase: int,
    min_lowercase: int,
    min_digits: int,
    min_specials: int,
    blocklist: str,
    allow_repeating: bool,
) -> str:
    charspace = Charspace(blocklist=blocklist)
    try_password = Candidate("")

    while not all(
        [
            True
            and try_password.uppers >= min_uppercase
            and try_password.lowers >= min_lowercase
            and try_password.digits >= min_digits
            and try_password.specials >= min_specials
            and (allow_repeating or not try_password.has_repeating)
        ]
    ):
        try_password = Candidate(generate(charspace.charset, min_length))

    return str(try_password)


@deal.has("random")
@deal.raises()
@deal.pre(
    validator=lambda charset, pass_length: pass_length > 0,
    message="pass_length must be greater than zero.",
    exception=ValueError,
)
@deal.pre(
    validator=lambda charset, pass_length: pass_length <= 512,
    message="pass_length cannot be greater than 512.",
    exception=ValueError,
)
@deal.pre(
    validator=lambda charset, pass_length: len("".join(charset)) > 0,
    message="charset must have positive len.",
    exception=ValueError,
)
@deal.ensure(
    lambda charset, pass_length, result: len(result) == pass_length,
    message="function return value len must equal requested pass_length.",
)
@deal.ensure(
    lambda charset, pass_length, result: all(
        char in "".join(charset) for char in result
    ),
    message="function return value must be "
    "composed of characters in the charset",
)
def generate(charset: str, pass_length: int) -> str:
    """Return a cryptographically secure password of length pass_length using
    characters only from the given charset. Max pass_length is 512."""
    return "".join(
        secrets.choice("".join(charset)) for i in range(pass_length)
    )
