"""Provide user settings capsule."""

from dataclasses import dataclass


@dataclass
class Settings:
    """Settings object."""

    length: int
    min_uppercase: int
    min_lowercase: int
    min_digits: int
    min_specials: int
    specials: str
    blocklist: str
    allow_repeating: bool
