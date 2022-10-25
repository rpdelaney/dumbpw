import os

import deal
from hypothesis import HealthCheck, settings

from dumbpw.engine import generate

settings.register_profile(
    "CI",
    suppress_health_check=(HealthCheck.too_slow,),
)
if os.getenv("CI", False):
    settings.load_profile("CI")


@deal.cases(
    func=generate,
)
def test_generate(case: deal.TestCase) -> None:
    case()
