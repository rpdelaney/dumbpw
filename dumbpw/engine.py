"""Provide an engine for finding a good dumb password."""

import secrets

import deal

from dumbpw.candidate import Candidate
from dumbpw.charspace import Charspace
from dumbpw.constants import DEFAULT_EXTRAS, PASSWORD_LENGTH_MAX
from dumbpw.errors import DumbValueError
from dumbpw.settings import Settings


deal.module_load(deal.pure)


@deal.safe
@deal.has("random")
@deal.pre(
    lambda _: (
        _.settings.min_uppercase
        + _.settings.min_lowercase
        + _.settings.min_digits
        + _.settings.min_specials
        <= _.settings.length
    ),
    exception=DumbValueError,
    message="You cannot request more characters than the password length.",
)
@deal.pre(
    validator=lambda _: _.settings.length <= PASSWORD_LENGTH_MAX,
    exception=DumbValueError,
    message=f"length cannot be greater than {PASSWORD_LENGTH_MAX}.",
)
@deal.pre(
    lambda _: _.settings.length > 0,
    message="length must be greater than zero.",
)
@deal.pre(
    lambda _: not (_.settings.min_specials > 0 and _.settings.specials == ""),
    exception=DumbValueError,
    message="Special characters required from empty character set.",
)
@deal.pre(
    lambda _: (
        not _.settings.blocklist
        or not _.settings.specials
        or all(c not in _.settings.blocklist for c in _.settings.specials)
    ),
    exception=DumbValueError,
    message="Required special characters in the blocklist.",
)
@deal.ensure(
    lambda _: _.result.uppers >= _.settings.min_uppercase,
    message="Not enough uppercase characters in result.",
)
@deal.ensure(
    lambda _: _.result.lowers >= _.settings.min_lowercase,
    message="Not enough lowercase characters in result.",
)
@deal.ensure(
    lambda _: _.result.digits >= _.settings.min_digits,
    message="Not enough digit characters in result.",
)
@deal.ensure(
    lambda _: _.result.specials >= _.settings.min_specials,
    message="Not enough special characters in result.",
)
@deal.ensure(
    lambda _: _.settings.allow_repeating or not _.result.has_repeating,
    message="Repeating characters are not allowed.",
)
@deal.ensure(
    lambda _: len(_.result) == _.settings.length,
    message="The returned value len must equal the requested length.",
)
def search(settings: Settings) -> Candidate:
    """Search for a password that meets the given requirements."""
    charspace = Charspace(
        blocklist=settings.blocklist,
        extras=DEFAULT_EXTRAS
        if settings.specials is None
        else settings.specials,
    )
    candidate = Candidate("")

    candidate.extend(
        secrets.choice(charspace.digits) for _ in range(settings.min_digits)
    )
    candidate.extend(
        secrets.choice(charspace.uppers) for _ in range(settings.min_uppercase)
    )
    candidate.extend(
        secrets.choice(charspace.lowers) for _ in range(settings.min_lowercase)
    )
    candidate.extend(
        secrets.choice(charspace.extras)
        for _ in range(settings.min_specials)
        if charspace.extras
    )

    while len(candidate) < settings.length:
        choice = secrets.choice(charspace.charset)
        if (
            not candidate
            or settings.allow_repeating
            or candidate[-1] != choice
        ):
            candidate += choice

    # TODO: test this is done at least once
    password = candidate.shuffled()

    # TODO: abstract this and make it safer.
    # e.g. 'aaaab' will loop forever
    while not settings.allow_repeating and password.has_repeating:
        password = Candidate(str(password.shuffled()))

    return password
