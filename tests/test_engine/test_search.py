import string

import deal
from hypothesis import HealthCheck, settings
from hypothesis import strategies as strats

from dumbpw import engine


settings.register_profile(
    "CI",
    suppress_health_check=(HealthCheck.too_slow,),
)
settings.load_profile("CI")


@deal.cases(
    func=engine.search,
    kwargs={
        "length": 30,
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
        "blocklist": strats.text(
            alphabet=string.punctuation,
            min_size=0,
            max_size=3,
        ),
    },
)
def test_search(case: deal.TestCase) -> None:
    case()
