"""Provide an engine for finding a good dumb password."""

import deal

from dumbpw.candidate import Candidate
from dumbpw.charspace import Charspace
from dumbpw.constants import DEFAULT_EXTRAS, PASSWORD_LENGTH_MAX
from dumbpw.errors import DumbValueError
from dumbpw.settings import Settings


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
        extras=settings.specials or DEFAULT_EXTRAS,
    )
    candidate = Candidate(["" for _ in range(settings.length)])

    args = [
        (settings.min_digits, charspace.digits_shuffled()),
        (settings.min_uppercase, charspace.uppers_shuffled()),
        (settings.min_lowercase, charspace.lowers_shuffled()),
        (settings.min_specials, charspace.extras_shuffled()),
    ]
    for count, charstack in args:
        candidate.scatter(
            count=count,
            charstack=charstack,
            allow_repeating=settings.allow_repeating,
        )

    candidate.scatter(
        count=len(candidate.voids),
        charstack=charspace.charset_shuffled(),
        allow_repeating=settings.allow_repeating,
    )

    return candidate
