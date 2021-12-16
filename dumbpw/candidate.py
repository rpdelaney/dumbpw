import string


class Candidate:
    def __init__(self, password: str) -> None:
        self._password = password

    def _count_string_type(self, haystack: str) -> int:
        """Return a count of how many characters in the password are part of
        the haystack."""
        return sum(1 for char in self._password if char in haystack)

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

    def __len__(self) -> int:
        return len(self._password)

    def __str__(self) -> str:
        return self._password
