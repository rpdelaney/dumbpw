import sys

import click

from .candidate import Candidate
from .charspace import Charspace
from .pwgen import generate


@click.command(
    no_args_is_help=True,
)
@click.option(
    "--length",
    type=click.IntRange(min=1, max=512),
    help="The length of the password.",
)
@click.option(
    "--uppercase",
    type=int,
    default=1,
    show_default=True,
    help="The minimum number of uppercase characters.",
)
@click.option(
    "--lowercase",
    type=int,
    default=1,
    show_default=True,
    help="The minimum number of lowercase characters.",
)
@click.option(
    "--digits",
    type=int,
    default=1,
    show_default=True,
    help="The minimum number of digit characters.",
)
@click.option(
    "--specials",
    type=int,
    default=1,
    show_default=True,
    help="The minimum number of special characters.",
)
@click.option(
    "--blocklist",
    type=str,
    default="""'";""",
    show_default=True,
    help="Characters that may not be in the password.",
)
def cli(
    length: int,
    uppercase: int,
    lowercase: int,
    digits: int,
    specials: int,
    blocklist: str,
) -> int:
    # You can't request more stuff than you have room for
    # There is probably a better way to do this using Click
    local = locals()
    requests = sum(
        local[key]
        for key in local.keys()
        if key not in ("length", "blocklist")
    )
    if length < requests:
        print("You cannot request more characters than the password length.")
        return 1

    charspace = Charspace(blocklist=blocklist)
    try_password = Candidate("")

    while not all(
        [
            True
            and (try_password.uppers >= uppercase)
            and (try_password.lowers >= lowercase)
            and (try_password.digits >= digits)
            and (try_password.specials >= specials)
        ]
    ):
        try_password = Candidate(generate(charspace.charset, length))

    print(try_password)

    return 0


if __name__ == "__main__":
    sys.exit(cli())
