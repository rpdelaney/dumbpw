from dataclasses import dataclass
from typing import Set

import deal

deal.activate()
deal.module_load(deal.pure)

from .constants import (
    DEFAULT_DIGITS,
    DEFAULT_EXTRAS,
    DEFAULT_LOWERS,
    DEFAULT_UPPERS,
)


@dataclass(frozen=True)
class Charspace:
    blocklist: str = ""
    digits: str = DEFAULT_DIGITS
    extras: str = DEFAULT_EXTRAS
    lowers: str = DEFAULT_LOWERS
    uppers: str = DEFAULT_UPPERS

    @property
    @deal.pure
    def base_charset(self) -> Set[str]:
        return set(self.lowers + self.uppers + self.digits + self.extras)

    @property
    @deal.pure
    def charset(self) -> Set[str]:
        """De-duplicate the base charset, remove characters that are in the
        blocklist, and return a charset as a string.
        """
        return set(self.base_charset) - set(self.blocklist)
