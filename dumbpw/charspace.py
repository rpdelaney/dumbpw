"""Define a dataclass for rendering the character search space."""

from dataclasses import dataclass

import deal

from .constants import (
    DEFAULT_DIGITS,
    DEFAULT_EXTRAS,
    DEFAULT_LOWERS,
    DEFAULT_UPPERS,
)


deal.activate()
deal.module_load(deal.pure)


@dataclass(frozen=True)
class Charspace:
    """Define an object that calculates and renders character space."""

    blocklist: str = ""
    digits: str = DEFAULT_DIGITS
    extras: str = DEFAULT_EXTRAS
    lowers: str = DEFAULT_LOWERS
    uppers: str = DEFAULT_UPPERS

    @property
    @deal.pure
    def base_charset(self) -> set[str]:
        """Calculate the base (unprocessed) charset."""
        return set(self.lowers + self.uppers + self.digits + self.extras)

    @property
    @deal.pure
    def charset(self) -> set[str]:
        """De-duplicate the base charset.

        Remove characters that are in the blocklist, and return a
        charset as a string.
        """
        return set(self.base_charset) - set(self.blocklist)
