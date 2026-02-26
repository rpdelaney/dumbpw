"""Provide an object for evaluating candidate passwords."""

import secrets
import string
from collections import Counter
from collections.abc import Iterator

import deal


class Candidate:
    """A subclass of str representing a password candidate.

    >>> password = Candidate("abcDEFG123!abc")
    >>> password.digits
    3
    >>> password.specials
    1
    >>> password.uppers
    4
    >>> password.lowers
    6
    >>> password.has_duplicates
    True
    >>> password.has_repeating
    False
    >>> password.must_repeat
    False
    """

    __slots__ = ("_text",)

    @deal.pure
    def __init__(self, /, text: str | list[str]) -> None:
        """Initialize the Candidate object."""
        self._text: list[str] = list(text)

    @deal.pure
    def __repr__(self) -> str:
        """Return a representation of the Candidate.

        >>> Candidate("")
        Candidate([])
        >>> Candidate("abc")
        Candidate(['a', 'b', 'c'])
        >>> Candidate("a c")
        Candidate(['a', ' ', 'c'])
        """
        return f"{self.__class__.__name__}({self._text!r})"

    @deal.pure
    def __add__(self, other: str) -> "Candidate":
        """Handle addition operator.

        >>> Candidate("aa") + "bb"
        Candidate('aabb')
        >>> Candidate("aa") + Candidate("bb")
        Candidate('aabb')
        """
        return Candidate("".join(self._text + list(other)))

    @deal.pure
    def __eq__(self, other) -> bool:  # type: ignore[no-untyped-def,misc]
        """Check equality between self and other.

        >>> Candidate("aa") == Candidate("aa")
        True
        >>> Candidate("aa") == Candidate("ab")
        False
        >>> Candidate("aa") == "aa"
        True
        """
        return str(self) == str(other)

    @deal.pure
    def __hash__(self) -> int:
        """Return a hash of self."""
        return hash(str(self._text))

    @deal.pure
    def __len__(self) -> int:
        """Return the length of the string."""
        return len(self._text)

    @deal.pure
    def __str__(self) -> str:
        """Return the plain text of the string."""
        return "".join(self._text)

    @deal.pure
    def __iter__(self) -> Iterator[str]:
        """Iterate over the text."""
        yield from self._text

    @deal.raises(IndexError)
    def __getitem__(self, item: int) -> str:
        """Provide subscriptability."""
        return self._text[item]

    @deal.raises(IndexError)
    def __setitem__(self, item: int, value: str) -> None:
        """Provide item assignment."""
        self._text[item] = value

    @deal.raises(IndexError)
    def __delitem__(self, item: int) -> None:
        """Provide item deletion."""
        del self._text[item]

    @property
    @deal.pure
    def must_repeat(self) -> bool:
        """Return True if the text cannot construct a non-repeating string."""
        f_max: int = max(Counter(self._text).values())
        limit: int = len(self._text) // 2
        return f_max >= limit

    def shuffled(self) -> "Candidate":
        """Cryptographically shuffle the string."""
        new_password = list(self._text)
        secrets.SystemRandom().shuffle(new_password)
        return Candidate("".join(new_password))

    @deal.pure
    @deal.post(
        lambda result: result >= 0,
        message="Count cannot be negative.",
    )
    def _count_string_type(self, haystack: str) -> int:
        """Count how many characters in the password are part of the haystack.

        >>> Candidate("")._count_string_type(string.ascii_lowercase)
        0
        >>> Candidate("123")._count_string_type(string.ascii_lowercase)
        0
        >>> Candidate("abcDEFG123!")._count_string_type(string.ascii_lowercase)
        3
        >>> Candidate("abcDEFG123!")._count_string_type(string.ascii_uppercase)
        4
        >>> Candidate("abcDEFG123!")._count_string_type(string.punctuation)
        1
        """
        return sum(1 for char in self._text if char in haystack)

    @property
    @deal.pure
    @deal.post(
        lambda result: result >= 0,
        message="Count cannot be negative.",
    )
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
    @deal.pure
    @deal.post(
        lambda result: result >= 0,
        message="Count cannot be negative.",
    )
    def specials(self) -> int:
        r"""Return a count of the ASCII punctuation characters in the password.

        >>> Candidate("").specials
        0
        >>> Candidate("abc").specials
        0
        >>> Candidate(r"abc%^*.").specials
        4
        >>> Candidate(r"a\bc").specials
        1
        """
        return self._count_string_type(string.punctuation)

    @property
    @deal.pure
    @deal.post(
        lambda result: result >= 0,
        message="Count cannot be negative.",
    )
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
    @deal.pure
    @deal.post(
        lambda result: result >= 0,
        message="Count cannot be negative.",
    )
    def lowers(self) -> int:
        """Return a count of the ASCII lowercase characters in the password.

        >>> Candidate("").lowers
        0
        >>> Candidate("abc").lowers
        3
        >>> Candidate("ABc").lowers
        1
        >>> Candidate("ABC").lowers
        0
        """
        return self._count_string_type(string.ascii_lowercase)

    @property
    @deal.pure
    def has_duplicates(self) -> bool:
        """Return if the password has duplicate characters.

        >>> Candidate("").has_duplicates
        False
        >>> Candidate("ABC").has_duplicates
        False
        >>> Candidate("ABA").has_duplicates
        True
        >>> Candidate("ABB").has_duplicates
        True
        """
        return len(set(self._text)) != len(self._text) if self._text else False

    @property
    @deal.pure
    def has_repeating(self) -> bool:
        """Return if the password has repeating characters.

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
        >>> Candidate("ABA").has_repeating
        False
        >>> Candidate("8[z]>").has_repeating
        False
        """
        return any(
            self._text[i] == self._text[i - 1]
            for i in range(1, len(self._text))
        )

    @deal.pure
    @deal.ensure(
        lambda self, result: self == result and self is not result,
        message="Must return a copy.",
    )
    def copy(self) -> "Candidate":
        """Return a copy of self."""
        return Candidate(self._text)

    @deal.safe
    def extend(self, iterator: Iterator[str]) -> None:
        """Extend the password by taking values from an iterator.

        >>> c = Candidate("")
        >>> c.extend(x for x in ["a", "b", "c"])
        >>> c._text == ["a", "b", "c"]
        True
        >>> c = Candidate("123")
        >>> c.extend(x for x in ["a", "b", "c"])
        >>> c._text == ["1", "2", "3", "a", "b", "c"]
        True
        """
        for c in iterator:
            self._text += c
