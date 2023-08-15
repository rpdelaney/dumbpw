import os

import deal
from hypothesis import HealthCheck, settings

from dumbpw.engine import generate

if os.environ.get("CI"):
    settings.register_profile(
        "CI",
        suppress_health_check=(HealthCheck.too_slow,),
    )
    settings.load_profile("CI")
    ci_settings = settings.from_profile("CI")
else:
    ci_settings = settings()


@ci_settings
@deal.cases(
    func=generate,
)
def test_generate(case: deal.TestCase) -> None:
    case()
