"""Provide an object for evaluating candidate passwords."""

import string

import deal


deal.activate()
deal.module_load(deal.pure)


class Candidate(str):
    """A subclass of str representing a password candidate.

    >>> password = Candidate("abcDEFG123!")
    >>> print(password.digits)
    3
    >>> print(password.specials)
    1
    >>> print(password.uppers)
    4
    >>> print(password.lowers)
    3
    >>> print(password.has_duplicates)
    False
    >>> print(password.has_repeating)
    False
    """

    __slots__ = ("password",)

    @deal.pure
    def __init__(self, /, password: str) -> None:
        """Initialize the Candidate object."""
        self.password = password
        return  # noqa: PLR1711

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
        return sum(1 for char in self.password if char in haystack)

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
        >>> Candidate(r"a\\bc").specials
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
        return (
            len(set(self.password)) != len(self.password)
            if self.password
            else False
        )

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
        """
        return any(
            self.password[i] == self.password[i - 1]
            for i in range(1, len(self.password))
        )

    @deal.pure
    @deal.ensure(
        lambda self, result: result == self and result is not self,
        message="Must return a copy.",
    )
    def copy(self) -> "Candidate":
        """Return a copy of self."""
        return Candidate(self.password)
