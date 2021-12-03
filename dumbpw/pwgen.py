import secrets

import deal


@deal.has()
@deal.pure
@deal.raises(IndexError)
@deal.reason(
    event=IndexError,
    validator=lambda keyspace, pass_length: len(keyspace) < 1,
)
def _generate(keyspace: str, pass_length: int) -> str:
    candidate: str = "".join(
        secrets.choice(keyspace) for i in range(pass_length)
    )

    return candidate
