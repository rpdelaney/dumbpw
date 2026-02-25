"""Define a dataclass for rendering the character search space."""

import secrets

import deal

from dumbpw.constants import (
    DEFAULT_DIGITS,
    DEFAULT_EXTRAS,
    DEFAULT_LOWERS,
    DEFAULT_UPPERS,
)


deal.module_load(deal.pure)


class Charspace:
    """Define an object that calculates and renders character space."""

    def __init__(
        self,
        *,
        blocklist: str = "",
        digits: str = DEFAULT_DIGITS,
        extras: str = DEFAULT_EXTRAS,
        lowers: str = DEFAULT_LOWERS,
        uppers: str = DEFAULT_UPPERS,
    ) -> None:
        """Initialize a Charspace."""
        self._blocklist = blocklist
        self._digits = digits
        self._extras = extras
        self._lowers = lowers
        self._uppers = uppers

    @deal.pure
    def __repr__(self) -> str:
        """Return a representation."""
        return f"{self.__class__.__name__}({''.join(sorted(self.charset))!r})"

    @deal.pure
    def __str__(self) -> str:
        """Return the charspace formatted as a string."""
        return "".join(sorted(self.charset))

    def __getitem__(self, item: int) -> str:
        """Provide subscriptability."""
        return str(self)[item]

    @property
    @deal.pure
    def base_charset(self) -> set[str]:
        """Calculate the base (unprocessed) charset."""
        return set(self._lowers + self._uppers + self._digits + self._extras)

    @property
    @deal.pure
    def charset(self) -> str:
        """De-duplicate the base charset.

        Remove characters that are in the blocklist, and return a
        charset as a string.
        """
        return "".join(set(self.base_charset) - set(self._blocklist))

    @property
    @deal.pure
    def digits(self) -> str:
        """Return the digits that aren't blocked."""
        return "".join(
            char for char in self._digits if char not in self._blocklist
        )

    @property
    @deal.pure
    def extras(self) -> str:
        """Return the extras that aren't blocked."""
        return "".join(
            char for char in self._extras if char not in self._blocklist
        )

    @property
    @deal.pure
    def lowers(self) -> str:
        """Return the lowers that aren't blocked."""
        return "".join(
            char for char in self._lowers if char not in self._blocklist
        )

    @property
    @deal.pure
    def uppers(self) -> str:
        """Return the uppers that aren't blocked."""
        return "".join(
            char for char in self._uppers if char not in self._blocklist
        )

    @deal.pure
    def charset_shuffled(self) -> str:
        """Return a cryptographically shuffled charset."""
        result = list(self.charset)
        secrets.SystemRandom().shuffle(result)
        return str(result)
