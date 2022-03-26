import string
from dataclasses import dataclass


@dataclass(frozen=True)
class Charspace:
    blocklist: str = ""
    digits: str = string.digits
    extras: str = string.punctuation
    lowers: str = string.ascii_lowercase
    uppers: str = string.ascii_uppercase

    @property
    def base_charset(self) -> str:
        return self.lowers + self.uppers + self.digits + self.extras

    @property
    def charset(self) -> str:
        """De-duplicate the base charset, remove characters that are in the
        blocklist, and return a charset as a string."""
        return "".join(
            {char for char in self.base_charset if char not in self.blocklist}
        )
