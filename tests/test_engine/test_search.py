import string

import deal
from hypothesis import HealthCheck, settings
from hypothesis import strategies as strats

from dumbpw import engine
from dumbpw.constants import DEFAULT_BLOCKS, PASSWORD_LENGTH_MIN
from dumbpw.settings import Settings


settings.register_profile(
    "CI",
    suppress_health_check=(HealthCheck.too_slow,),
)
settings.load_profile("CI")

SETTINGS_STRATEGY = strats.builds(
    Settings,
    allow_repeating=strats.booleans(),
    length=strats.integers(min_value=PASSWORD_LENGTH_MIN, max_value=10),
    min_uppercase=strats.integers(min_value=0, max_value=1),
    min_lowercase=strats.integers(min_value=0, max_value=1),
    min_digits=strats.integers(min_value=0, max_value=1),
    min_specials=strats.integers(min_value=0, max_value=1),
    specials=strats.text(alphabet=string.punctuation, min_size=0, max_size=1),
    blocklist=strats.just(DEFAULT_BLOCKS),
)


@deal.cases(
    func=engine.search,
    kwargs={"settings": SETTINGS_STRATEGY},
)
def test_search(case: deal.TestCase) -> None:
    case()
