import string


class Candidate(str):
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
