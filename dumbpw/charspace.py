from dataclasses import dataclass

import deal

deal.activate()

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

    @property  # type: ignore[misc]
    @deal.pure
    def base_charset(self) -> str:
        return self.lowers + self.uppers + self.digits + self.extras

    @property  # type: ignore[misc]
    @deal.pure
    def charset(self) -> str:
        """De-duplicate the base charset, remove characters that are in the
        blocklist, and return a charset as a string.
        """
        return "".join(
            {char for char in self.base_charset if char not in self.blocklist}
        )
