import string
from typing import Generator


class Charspace:
    def __init__(
        self,
        blocklist: str = "",
        extras: str = string.punctuation,
        uppers: str = string.ascii_uppercase,
        lowers: str = string.ascii_lowercase,
        digits: str = string.digits,
    ) -> None:
        self._blocklist = blocklist
        self._extras = extras
        self._uppers = uppers
        self._lowers = lowers
        self._digits = digits

    @property
    def base_charset(self) -> str:
        return self._lowers + self._uppers + self._digits + self._extras

    @property
    def charset(self) -> str:
        """De-duplicate the base charset, remove characters that are in the
        blocklist, and return a charset as a string."""
        return "".join(
            {char for char in self.base_charset if char not in self._blocklist}
        )

    @property
    def blocklist(self) -> str:
        return self._blocklist

    @blocklist.setter
    def blocklist(self, new_blocklist: str) -> None:
        self._blocklist = new_blocklist

    @property
    def extras(self) -> str:
        return self._extras

    @extras.setter
    def extras(self, new_extras: str) -> None:
        self._extras = new_extras

    @property
    def lowers(self) -> str:
        return self._lowers

    @lowers.setter
    def lowers(self, new_lowers: str) -> None:
        self._lowers = new_lowers

    @property
    def uppers(self) -> str:
        return self._uppers

    @uppers.setter
    def uppers(self, new_uppers: str) -> None:
        self._uppers = new_uppers

    @property
    def digits(self) -> str:
        return self._digits

    @digits.setter
    def digits(self, new_digits: str) -> None:
        self._digits = new_digits

    def __iter__(self) -> Generator[tuple[str, str], None, None]:
        yield "base_charset", self.base_charset
        yield "charset", self.charset
        yield "blocklist", self.blocklist
        yield "extras", self.extras
        yield "lowers", self.lowers
        yield "uppers", self.uppers
        yield "digits", self.digits
