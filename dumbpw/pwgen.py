import secrets

import deal


@deal.has("random")
@deal.pure
@deal.raises()
def _generate(keyspace: str, pass_length: int) -> str:
    """Return a cryptographically secure password of length pass_length using
    characters only from the given keyspace."""
    return "".join(secrets.choice(keyspace) for i in range(pass_length))
