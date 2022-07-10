import string

import deal


class Candidate(str):
    @deal.pure
    def __init__(self, /, password: str) -> None:
        self.password = password
        return

    @deal.pure
    def _count_string_type(self, haystack: str) -> int:
        """Return a count of how many characters in the password are part of
        the haystack.
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

    @property  # type: ignore[misc]
    @deal.pure
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

    @property  # type: ignore[misc]
    @deal.pure
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

    @property  # type: ignore[misc]
    @deal.pure
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

    @property  # type: ignore[misc]
    @deal.pure
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

    @property  # type: ignore[misc]
    @deal.pure
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
            len(set(self.password)) != len(self.password)
            if self.password
            else False
        )

    @property  # type: ignore[misc]
    @deal.pure
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
        for index in range(1, len(self.password)):
            if self.password[index] == self.password[index - 1]:
                return True
        else:
            return False

    @deal.pure
    def copy(self) -> "Candidate":
        """Return a copy of self.
        >>> cd = Candidate("A")
        >>> cp = cd.copy()
        >>> cd == cp
        True
        >>> cp is cd
        False
        """
        return Candidate(self.password)
