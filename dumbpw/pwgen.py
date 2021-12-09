import secrets
from typing import FrozenSet, Set

import deal


@deal.has("random")
@deal.pure
@deal.raises()
@deal.pre(
    validator=lambda keyspace, pass_length: pass_length > 0,
    message="pass_length must be greater than zero.",
    exception=ValueError,
)
@deal.pre(
    validator=lambda keyspace, pass_length: len("".join(keyspace)) > 0,
    message="keyspace must have positive len.",
    exception=ValueError,
)
@deal.ensure(
    lambda keyspace, pass_length, result: len(result) == pass_length,
    message="function return value len must equal requested pass_length.",
)
@deal.ensure(
    lambda keyspace, pass_length, result: all(
        char in "".join(keyspace) for char in result
    ),
    message="function return value must be "
    "composed of characters in the keyspace",
)
def generate(keyspace: Set[str] | FrozenSet[str], pass_length: int) -> str:
    """Return a cryptographically secure password of length pass_length using
    characters only from the given keyspace."""
    return "".join(
        secrets.choice("".join(keyspace)) for i in range(pass_length)
    )
