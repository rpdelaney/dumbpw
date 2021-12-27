import secrets

import deal

deal.activate()

from .candidate import Candidate
from .charspace import Charspace
from .constants import MAX_PASSWORD_LENGTH


@deal.pre(
    validator=lambda _: _.min_uppercase
    + _.min_lowercase
    + _.min_digits
    + _.min_specials
    <= _.length,
    exception=ValueError,
    message="You cannot request more characters than the password length.",
)
@deal.pre(
    validator=lambda _: _.length <= MAX_PASSWORD_LENGTH,
    exception=ValueError,
    message=f"The maximum password length is {MAX_PASSWORD_LENGTH}.",
)
@deal.pre(
    validator=lambda _: _.length > 0,
    message="length must be greater than zero.",
    exception=ValueError,
)
@deal.ensure(
    lambda _: len(_.result) == _.length,
    message="The returned password length must equal the requested length.",
)
def search(
    length: int,
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
            and len(try_password) == length
        ]
    ):
        try_password = Candidate(generate(charspace.charset, length))

    return str(try_password)


@deal.has("random")
@deal.pre(
    validator=lambda charset, pass_length: pass_length > 0,
    message="pass_length must be greater than zero.",
    exception=ValueError,
)
@deal.pre(
    validator=lambda charset, pass_length: pass_length <= MAX_PASSWORD_LENGTH,
    message=f"pass_length cannot be greater than {MAX_PASSWORD_LENGTH}.",
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
    characters only from the given charset."""
    return "".join(
        secrets.choice("".join(charset)) for i in range(pass_length)
    )
