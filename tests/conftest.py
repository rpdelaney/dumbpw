import os

from hypothesis import HealthCheck, settings

settings.register_profile("CI", suppress_health_check=(HealthCheck.too_slow,))

if os.getenv("CI", False):
    settings.load_profile("CI")
