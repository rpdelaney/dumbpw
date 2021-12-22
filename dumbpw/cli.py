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
    "--length",
    type=click.IntRange(min=1, max=512),
    help="The length of the password.",
)
@click.option(
    "--uppercase",
    type=int,
    default=1,
    help="The minimum number of uppercase characters.",
)
@click.option(
    "--lowercase",
    type=int,
    default=1,
    help="The minimum number of lowercase characters.",
)
@click.option(
    "--digits",
    type=int,
    default=1,
    help="The minimum number of digit characters.",
)
@click.option(
    "--specials",
    type=int,
    default=1,
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
    length: int,
    uppercase: int,
    lowercase: int,
    digits: int,
    specials: int,
    blocklist: str,
    allow_repeating: bool,
) -> int:
    # You can't request more stuff than you have room for
    # There is probably a better way to do this using Click
    requests = uppercase + lowercase + digits + specials
    if length < requests:
        print("You cannot request more characters than the password length.")
        return 1

    charspace = Charspace(blocklist=blocklist)
    try_password = Candidate("")

    while not all(
        [
            True
            and try_password.uppers >= uppercase
            and try_password.lowers >= lowercase
            and try_password.digits >= digits
            and try_password.specials >= specials
            and (allow_repeating or not try_password.has_duplicates)
        ]
    ):
        try_password = Candidate(generate(charspace.charset, length))

    print(try_password)

    return 0


if __name__ == "__main__":
    sys.exit(cli())
