import fileinput
import sys
from typing import NoReturn

import click
import deal

deal.activate()

from .constants import DEFAULT_BLOCKS, PASSWORD_LENGTH_MAX, PASSWORD_LENGTH_MIN
from .engine import search
from .exceptions import DumbValueError


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
def cli(
    length: int,
    min_uppercase: int,
    min_lowercase: int,
    min_digits: int,
    min_specials: int,
    specials: str,
    blocklist: str,
    allow_repeating: bool,
) -> NoReturn:
    if specials == "-":
        specials = "".join(char for char in fileinput.input(files="-")).strip()

    try:
        try_password = search(
            length=length,
            min_uppercase=min_uppercase,
            min_lowercase=min_lowercase,
            min_digits=min_digits,
            min_specials=min_specials,
            specials=specials,
            blocklist=blocklist,
            allow_repeating=allow_repeating,
        )
    except DumbValueError as ve:
        print(ve, file=sys.stderr)
        sys.exit(1)

    print(try_password)

    sys.exit(0)
