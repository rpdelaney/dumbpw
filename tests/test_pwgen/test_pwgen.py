import deal
from hypothesis import strategies as strats

import dumbpw.pwgen as pwgen


@deal.cases(
    func=pwgen.generate,
)
def test_generate(case: deal.TestCase) -> None:
    case()


@deal.cases(
    func=pwgen.search,
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
    },
)
def test_search(case: deal.TestCase) -> None:
    case()
