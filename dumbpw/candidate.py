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
        """Return a count of the ASCII digit characters in the password.
        >>> Candidate("").digits
        0
        >>> Candidate("abc").digits
        0
        >>> Candidate("123").digits
        3
        >>> Candidate("0a").digits
        1
        >>> Candidate("0#").digits
        1
        """
        return self._count_string_type(string.digits)

    @property
    def specials(self) -> int:
        """Return a count of the ASCII punctuation characters in the password.
        >>> Candidate("").specials
        0
        >>> Candidate("abc").specials
        0
        >>> Candidate(r"abc%^*.").specials
        4
        >>> Candidate(r"a\\bc").specials
        1
        """
        return self._count_string_type(string.punctuation)

    @property
    def uppers(self) -> int:
        """Return a count of the ASCII uppercase characters in the password.
        >>> Candidate("").uppers
        0
        >>> Candidate("abc").uppers
        0
        >>> Candidate("ABc").uppers
        2
        >>> Candidate("ABC").uppers
        3
        """
        return self._count_string_type(string.ascii_uppercase)

    @property
    def lowers(self) -> int:
        return self._count_string_type(string.ascii_lowercase)

    @property
    def has_duplicates(self) -> bool:
        """Return True if the password has duplicate characters, otherwise
        False.
        >>> Candidate("").has_duplicates
        False
        >>> Candidate("ABC").has_duplicates
        False
        >>> Candidate("ABA").has_duplicates
        True
        >>> Candidate("ABB").has_duplicates
        True
        """
        return (
            any(self._password.count(c) != 1 for c in self._password)
            if len(self._password)
            else False
        )

    @property
    def has_repeating(self) -> bool:
        """Return True if the password has repeating characters, otherwise
        False.
        >>> Candidate("").has_repeating
        False
        >>> Candidate("A").has_repeating
        False
        >>> Candidate("ABA").has_repeating
        False
        >>> Candidate("AAB").has_repeating
        True
        >>> Candidate("ABB").has_repeating
        True
        """
        for index in range(1, len(self._password)):
            if self._password[index] == self._password[index - 1]:
                return True
        else:
            return False

    def copy(self) -> "Candidate":
        """Return a copy of self.
        >>> cd = Candidate("A")
        >>> cp = cd.copy()
        >>> cd == cp
        True
        >>> cp is cd
        False
        """
        return Candidate(self._password)

    def __len__(self) -> int:
        """Return length of the password, for len().
        >>> cd = Candidate("hi")
        >>> len(cd)
        2
        """
        return len(self._password)

    def __str__(self) -> str:
        """Convert to a string, for str().
        >>> cd = Candidate("hi")
        >>> str(cd)
        'hi'
        """
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
        """Supports subscription of the password.
        >>> cd = Candidate("ABC")
        >>> cd[0]
        'A'
        >>> cd[2]
        'C'
        >>> cd[1:]
        'BC'
        >>> cd[:1]
        'A'
        >>> cd[:-1]
        'AB'
        >>> 'B' in cd
        True
        >>> 'D' not in cd
        True
        """
        return self._password[item]

    def __lt__(self, lvalue: str) -> bool:
        """Supports the '<' comparison operator.
        >>> Candidate("B") < Candidate("A")
        False
        >>> Candidate("A") < Candidate("B")
        True
        >>> Candidate("A") < Candidate("A")
        False
        """
        return bool(self._password < lvalue)

    def __le__(self, lvalue: str) -> bool:
        """Supports the '<=' comparison operator.
        >>> Candidate("B") <= Candidate("A")
        False
        >>> Candidate("A") <= Candidate("B")
        True
        >>> Candidate("A") <= Candidate("A")
        True
        """
        return bool(self._password <= lvalue)

    def __eq__(self, lvalue: Any) -> bool:
        """Supports the '==' comparison operator.
        >>> Candidate("A") == Candidate("B")
        False
        >>> Candidate("A") == "B"
        False
        >>> Candidate("A") == Candidate("A")
        True
        >>> Candidate("A") == "A"
        True
        """
        return bool(str(self) == lvalue)

    def __ne__(self, lvalue: Any) -> bool:
        """Supports the '!=' comparison operator.
        >>> Candidate("A") != Candidate("B")
        True
        >>> Candidate("A") != Candidate("A")
        False
        """
        return bool(self._password != lvalue)

    def __gt__(self, lvalue: str) -> bool:
        """Supports the '>' comparison operator.
        >>> Candidate("B") > Candidate("A")
        True
        >>> Candidate("A") > Candidate("B")
        False
        >>> Candidate("A") > Candidate("A")
        False
        """
        return bool(self._password > lvalue)

    def __ge__(self, lvalue: str) -> bool:
        """Supports the '>=' comparison operator.
        >>> Candidate("B") >= Candidate("A")
        True
        >>> Candidate("A") >= Candidate("B")
        False
        >>> Candidate("A") >= Candidate("A")
        True
        """
        return bool(self._password >= lvalue)

    def __add__(self, new_chars: str) -> "Candidate":
        """Supports the '+' operator.
        >>> Candidate("A") + "B"
        dumbpw.candidate.Candidate("AB")
        >>> Candidate("A") + Candidate("B")
        dumbpw.candidate.Candidate("AB")
        """
        return Candidate(str(self) + str(new_chars))
