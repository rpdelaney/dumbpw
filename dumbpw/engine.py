"""Provide an engine for finding a good dumb password."""

import secrets
import string

import deal

from .candidate import Candidate
from .charspace import Charspace
from .constants import PASSWORD_LENGTH_MAX
from .exceptions import DumbValueError
from .settings import Settings


deal.activate()
deal.module_load(deal.pure)


@deal.safe
@deal.has("random")
@deal.pre(
    validator=lambda _: _.length <= PASSWORD_LENGTH_MAX,
    exception=DumbValueError,
    message=f"length cannot be greater than {PASSWORD_LENGTH_MAX}.",
)
@deal.pre(
    lambda _: (
        _.min_uppercase + _.min_lowercase + _.min_digits + _.min_specials
        <= _.settings.length
    ),
    exception=DumbValueError,
    message="You cannot request more characters than the password length.",
)
@deal.pre(
    validator=lambda _: _.length <= PASSWORD_LENGTH_MAX,
    exception=DumbValueError,
    message=f"length cannot be greater than {PASSWORD_LENGTH_MAX}.",
)
@deal.pre(
    lambda _: _.length > 0,
    message="length must be greater than zero.",
)
@deal.pre(
    lambda _: _.settings.blocklist
    and all(c not in _.settings.blocklist for c in _.settings.specials),
    exception=DumbValueError,
    message=(
        "You cannot require a special character that is also in the blocklist."
    ),
)
@deal.ensure(
    lambda _: _.result.uppers >= _.min_uppercase,
    message="Not enough uppercase characters in result.",
)
@deal.ensure(
    lambda _: _.result.lowers >= _.min_lowercase,
    message="Not enough lowercase characters in result.",
)
@deal.ensure(
    lambda _: _.result.digits >= _.min_digits,
    message="Not enough digit characters in result.",
)
@deal.ensure(
    lambda _: _.result.specials >= _.min_specials,
    message="Not enough special characters in result.",
)
@deal.ensure(
    lambda _: _.result.has_repeating or not _.allow_repeating,
    message="Repeating characters are not allowed.",
)
@deal.ensure(
    lambda _: len(_.result) == _.length,
    message="The returned value len must equal the requested length.",
)
def search(settings: Settings) -> Candidate:
    """Search for a password that meets the given requirements."""
    charspace_args = {
        "blocklist": settings.blocklist,
        "extras": settings.specials
        if settings.specials
        else string.punctuation,
    }

    charspace = Charspace(**charspace_args)

    def is_valid_password(password: Candidate) -> bool:
        return (
            password.uppers >= settings.min_uppercase
            and password.lowers >= settings.min_lowercase
            and password.digits >= settings.min_digits
            and password.specials >= settings.min_specials
            and (settings.allow_repeating or not password.has_repeating)
            and len(password) == settings.length
        )

    try_password = Candidate("")

    while not is_valid_password(try_password):
        try_password = Candidate(
            generate(
                charset=charspace.charset,
                length=settings.length,
            )
        )

    return try_password


@deal.safe
@deal.has("random")
@deal.pre(
    validator=lambda _: _.length <= PASSWORD_LENGTH_MAX,
    message=f"length cannot be greater than {PASSWORD_LENGTH_MAX}.",
)
@deal.pre(
    lambda _: _.length > 0,
    message="length must be greater than zero.",
)
@deal.pre(
    lambda _: len("".join(_.charset)) > 0,
    message="charset must have positive len.",
)
@deal.ensure(
    lambda _: len(_.result) == _.length,
    message="The returned value len must equal the requested length.",
)
@deal.ensure(
    lambda _: all(char in "".join(_.charset) for char in _.result),
    message=(
        "function return value must be composed of characters in the charset"
    ),
)
def generate(*, charset: set[str], length: int) -> str:
    """Return a cryptographically secure password.

    The value must be of len length using characters only from the given
    charset.
    """
    return "".join(secrets.choice("".join(charset)) for i in range(length))
