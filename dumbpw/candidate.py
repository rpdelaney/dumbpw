import string
from typing import Any, Iterator


class Candidate:
    def __init__(self, password: str) -> None:
        self._password = password

    def _count_string_type(self, haystack: str) -> int:
        """Return a count of how many characters in the password are part of
        the haystack."""
        return sum(1 for char in self._password if char in haystack)

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, new_password: str) -> None:
        self._password = new_password

    @property
    def digits(self) -> int:
        return self._count_string_type(string.digits)

    @property
    def specials(self) -> int:
        return self._count_string_type(string.punctuation)

    @property
    def uppers(self) -> int:
        return self._count_string_type(string.ascii_uppercase)

    @property
    def lowers(self) -> int:
        return self._count_string_type(string.ascii_lowercase)

    @property
    def has_duplicates(self) -> bool:
        return (
            any(self._password.count(c) != 1 for c in self._password)
            if len(self._password)
            else False
        )

    @property
    def has_repeating(self) -> bool:
        for index in range(1, len(self._password)):
            if self._password[index] == self._password[index - 1]:
                return True
        else:
            return False

    def copy(self) -> "Candidate":
        return Candidate(self._password)

    def __len__(self) -> int:
        return len(self._password)

    def __str__(self) -> str:
        return self._password

    def __repr__(self) -> str:
        """Convert to a formal string, for repr().

        >>> cd = Candidate("hi")
        >>> repr(cd)
        'dumbpw.candidate.Candidate("hi")'
        """
        return '{}.{}("{}")'.format(
            self.__class__.__module__,
            self.__class__.__qualname__,
            self._password,
        )

    def __iter__(self) -> Iterator[str]:
        return iter(self._password)

    def __getitem__(self, item: int) -> str:
        return self._password[item]

    def __lt__(self, lvalue: str) -> bool:
        return bool(self._password < lvalue)

    def __le__(self, lvalue: str) -> bool:
        return bool(self._password <= lvalue)

    def __eq__(self, lvalue: Any) -> bool:
        return bool(self._password == lvalue)

    def __ne__(self, lvalue: Any) -> bool:
        return bool(self._password != lvalue)

    def __ge__(self, lvalue: str) -> bool:
        return bool(self._password >= lvalue)

    def __gt__(self, lvalue: str) -> bool:
        return bool(self._password > lvalue)

    def __add__(self, new_chars: str) -> "Candidate":
        return Candidate(self._password + new_chars)
