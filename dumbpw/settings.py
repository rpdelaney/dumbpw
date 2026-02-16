"""Provide user settings capsule."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Settings object."""

    allow_repeating: bool
    blocklist: str
    length: int
    min_digits: int
    min_lowercase: int
    min_specials: int
    min_uppercase: int
    specials: str
