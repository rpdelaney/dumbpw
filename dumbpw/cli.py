import sys

import click

from .candidate import Candidate
from .charspace import Charspace
from .pwgen import generate


@click.command(
    no_args_is_help=True,
)
@click.version_option()
@click.option(
    "--min_length",
    type=click.IntRange(min=1, max=512),
    help="The length of the password.",
)
@click.option(
    "--min_uppercase",
    type=int,
    default=0,
    help="The minimum number of uppercase characters.",
)
@click.option(
    "--min_lowercase",
    type=int,
    default=0,
    help="The minimum number of lowercase characters.",
)
@click.option(
    "--min_digits",
    type=int,
    default=0,
    help="The minimum number of digit characters.",
)
@click.option(
    "--min_specials",
    type=int,
    default=0,
    help="The minimum number of special characters.",
)
@click.option(
    "--blocklist",
    type=str,
    default="""'";""",
    show_default=True,
    help="Characters that may not be in the password.",
)
@click.option(
    "--allow-repeating/--reject-repeating",
    help="Allow or reject repeating characters in the password.",
    default=False,
    show_default=True,
)
def cli(
    min_length: int,
    min_uppercase: int,
    min_lowercase: int,
    min_digits: int,
    min_specials: int,
    blocklist: str,
    allow_repeating: bool,
) -> int:
    # You can't request more stuff than you have room for
    # There is probably a better way to do this using Click
    requests = min_uppercase + min_lowercase + min_digits + min_specials
    if min_length < requests:
        print("You cannot request more characters than the password length.")
        return 1

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

    print(try_password)

    return 0


if __name__ == "__main__":
    sys.exit(cli())
