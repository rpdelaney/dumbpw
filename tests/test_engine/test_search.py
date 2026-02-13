import string

import deal
import pytest
from hypothesis import HealthCheck, settings
from hypothesis import strategies as strats

from dumbpw import engine
from dumbpw.constants import DEFAULT_BLOCKS, PASSWORD_LENGTH_MIN
from dumbpw.errors import DumbValueError
from dumbpw.settings import Settings


settings.register_profile(
    "CI",
    suppress_health_check=(HealthCheck.too_slow,),
)
settings.load_profile("CI")

PROPERTY_STRATEGY = strats.builds(
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
    kwargs={"settings": PROPERTY_STRATEGY},
)
def test_search(case: deal.TestCase) -> None:
    case()


class TestPigeonholes:
    """Test handling of unreachable requirements."""

    def test_pigeonholes_small_charset(self):
        """engine.search raises DumbValueEror on too-short length."""
        settings = Settings(
            allow_repeating=True,
            length=5,
            min_uppercase=5,
            min_lowercase=5,
            min_digits=5,
            min_specials=5,
            specials="!@#$",
            blocklist="",
        )

        with pytest.raises(DumbValueError):
            engine.search(settings)
