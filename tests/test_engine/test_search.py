import string

import deal
from hypothesis import HealthCheck, settings
from hypothesis import strategies as strats

from dumbpw import engine
from dumbpw.settings import Settings


settings.register_profile(
    "CI",
    suppress_health_check=(HealthCheck.too_slow,),
)
settings.load_profile("CI")

SETTINGS_STRATEGY = strats.builds(
    Settings,
    allow_repeating=strats.booleans(),
    length=strats.just(30),
    min_uppercase=strats.integers(min_value=0, max_value=3),
    min_lowercase=strats.integers(min_value=0, max_value=3),
    min_digits=strats.integers(min_value=0, max_value=3),
    min_specials=strats.integers(min_value=0, max_value=3),
    specials=strats.text(alphabet=string.punctuation, min_size=0, max_size=3),
    blocklist=strats.just(""),
)


@deal.cases(
    func=engine.search,
    kwargs={"settings": SETTINGS_STRATEGY},
)
def test_search(case: deal.TestCase) -> None:
    case()
