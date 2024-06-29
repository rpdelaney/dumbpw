"""Create a command-line interface entrypoint."""

import fileinput
import sys
from typing import NoReturn

import click
import deal


deal.activate()

from .constants import (  # noqa: E402
    DEFAULT_BLOCKS,
    PASSWORD_LENGTH_MAX,
    PASSWORD_LENGTH_MIN,
)
from .engine import search  # noqa: E402
from .exceptions import DumbValueError  # noqa: E402
from .settings import Settings  # noqa: E402


@deal.has("io", "global", "stderr", "stdout")
@deal.raises(SystemExit, RuntimeError)
@click.command(
    no_args_is_help=True,
)
@click.version_option()
@click.option(
    "--min-uppercase",
    type=int,
    default=1,
    help="The minimum number of uppercase characters.",
)
@click.option(
    "--min-lowercase",
    type=int,
    default=1,
    help="The minimum number of lowercase characters.",
)
@click.option(
    "--min-digits",
    type=int,
    default=1,
    help="The minimum number of digit characters.",
)
@click.option(
    "--min-specials",
    type=int,
    default=0,
    help="The minimum number of special characters.",
)
@click.option(
    "--blocklist",
    type=str,
    default=DEFAULT_BLOCKS,
    show_default=True,
    help="Characters that may not be in the password.",
)
@click.option(
    "--allow-repeating/--reject-repeating",
    help="Allow or reject repeating characters in the password.",
    default=False,
    show_default=True,
)
@click.argument(
    "length",
    type=click.IntRange(
        min=PASSWORD_LENGTH_MIN,
        max=PASSWORD_LENGTH_MAX,
    ),
)
@click.option(
    "--specials",
    envvar="DUMBPW_SPECIALS",
    help=(
        "Non-alphanumeric characters that may be in the password. "
        "Pass '-' to read from standard input."
    ),
    default="",
)
def cli(  # noqa: PLR0913
    *,
    length: int,
    min_uppercase: int,
    min_lowercase: int,
    min_digits: int,
    min_specials: int,
    specials: str,
    blocklist: str,
    allow_repeating: bool,
) -> NoReturn:
    """A dumb password generator."""  # noqa: D401
    if specials == "-":
        specials = "".join(char for char in fileinput.input(files="-")).strip()

    settings = Settings(
        length=length,
        min_uppercase=min_uppercase,
        min_lowercase=min_lowercase,
        min_digits=min_digits,
        min_specials=min_specials,
        specials=specials,
        blocklist=blocklist,
        allow_repeating=allow_repeating,
    )
    try:
        try_password = search(settings)
    except DumbValueError as ve:
        print(ve, file=sys.stderr)
        sys.exit(1)

    print(try_password)

    sys.exit(0)
