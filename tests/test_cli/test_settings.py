from dataclasses import FrozenInstanceError

import pytest

from dumbpw.cli import Settings


def test_settings_frozen():
    """The instance is frozen."""
    settings = Settings(
        allow_repeating=True,
        blocklist="",
        length=0,
        min_digits=0,
        min_lowercase=0,
        min_specials=0,
        min_uppercase=0,
        specials="",
    )

    with pytest.raises(FrozenInstanceError):
        settings.allow_repeating = True
