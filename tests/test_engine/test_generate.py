import os

import deal
from hypothesis import HealthCheck, settings
from hypothesis import strategies as strats

from dumbpw.engine import generate


if os.environ.get("CI"):
    settings.register_profile(
        "CI",
        suppress_health_check=(HealthCheck.too_slow,),
    )
    settings.load_profile("CI")
    ci_settings = settings.get_profile("CI")
else:
    ci_settings = settings()


@deal.cases(
    func=generate,
    settings=ci_settings,
    kwargs={
        "length": strats.integers(min_value=1, max_value=16),
    },
)
def test_generate(case: deal.TestCase) -> None:
    case()
