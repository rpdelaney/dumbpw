import string
from typing import FrozenSet


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
    def charset(self) -> FrozenSet[str]:
        return frozenset(
            "".join(
                char
                for char in self.base_charset
                if char not in self._blocklist
            )
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
