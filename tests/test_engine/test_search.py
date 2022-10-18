import string

import deal
from hypothesis import strategies as strats

import dumbpw.engine as engine


@deal.cases(
    func=engine.search,
    kwargs={
        "min_uppercase": strats.integers(
            min_value=0,
            max_value=3,
        ),
        "min_lowercase": strats.integers(
            min_value=0,
            max_value=3,
        ),
        "min_digits": strats.integers(
            min_value=0,
            max_value=3,
        ),
        "min_specials": strats.integers(
            min_value=0,
            max_value=3,
        ),
        "specials": strats.text(
            alphabet=string.punctuation,
            min_size=0,
            max_size=3,
        ),
    },
)
def test_search(case: deal.TestCase) -> None:
    case()
