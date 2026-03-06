"""Provide an object for evaluating candidate passwords."""

import secrets
import string
from abc import ABC, abstractmethod
from collections.abc import Iterator

import deal

from dumbpw.errors import DumbConstraintError


class Slot(ABC):
    """Position in the password."""

    _value: str | None

    @property
    @abstractmethod
    def value(self) -> str | None:
        """Return the value."""

    @abstractmethod
    def __repr__(self) -> str:
        """Return a representation of self."""

    @abstractmethod
    def __str__(self) -> str:
        """Return a representation of self."""

    @abstractmethod
    def __bool__(self) -> bool:
        """Return the truthiness of the slot."""

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """Check equality between self and other."""

    @abstractmethod
    def __hash__(self) -> int:
        """Return the hash of self."""


class Void(Slot):
    """An empty slot in the password under construction.

    >>> v = Void()
    >>> v.value
    >>> bool(v)
    False
    >>> repr(v)
    'Void()'
    >>> str(v)
    '•'
    >>> v == Void()
    True
    >>> v == None
    False
    """

    def __init__(self) -> None:
        """Initialize a Void."""
        self._value = None

    @property
    def value(self) -> None:
        """Return None, as this is an empty slot."""
        return None

    def __repr__(self) -> str:
        """Return a representation of self."""
        return "Void()"

    def __str__(self) -> str:
        """Return a string of self._value."""
        return "•"

    def __bool__(self) -> bool:
        """Return False, since null values are falsy."""
        return False

    def __eq__(self, other: object) -> bool:
        """Check equality between self and other."""
        if not isinstance(other, Slot):
            return NotImplemented
        return self._value == other._value

    def __hash__(self) -> int:
        """Return the hash of self."""
        return hash(self._value)


class Char(Slot):
    """An occupied slot in the password under construction.

    >>> c = Char("a")
    >>> c.value
    'a'
    >>> bool(c)
    True
    >>> repr(c)
    "Char('a')"
    >>> str(c)
    'a'
    >>> c == Char("a")
    True
    >>> c == Char("b")
    False
    >>> c == Void()
    False
    >>> c == "a"
    False
    """

    @deal.pre(lambda self, value: len(value) == 1)  # noqa: ARG005
    def __init__(self, value: str) -> None:
        """Initialize a Char with a single character."""
        self._value: str = value

    @property
    def value(self) -> str:
        """Return the character in this slot."""
        return self._value

    def __str__(self) -> str:
        """Return a string of a char slot."""
        return self._value

    def __repr__(self) -> str:
        """Return a string representation of a character slot."""
        return f"Char('{self._value}')"

    def __bool__(self) -> bool:
        """Return True, since characters are truthy."""
        return True

    def __eq__(self, other: object) -> bool:
        """Check equality between self and other."""
        if not isinstance(other, Slot):
            return NotImplemented
        return self._value == other._value

    def __hash__(self) -> int:
        """Return the hash of self."""
        return hash(self._value)


class Candidate:
    """Password constructor.

    >>> cd = Candidate(
    ...     [
    ...         Char("a"),
    ...         Char("b"),
    ...         Char("c"),
    ...         Char("D"),
    ...         Char("E"),
    ...         Char("F"),
    ...         Char("G"),
    ...         Char("1"),
    ...         Char("2"),
    ...         Char("3"),
    ...         Char("!"),
    ...         Char("a"),
    ...         Char("b"),
    ...         Char("c"),
    ...     ]
    ... )
    >>> cd.digits
    3
    >>> cd.specials
    1
    >>> cd.uppers
    4
    >>> cd.lowers
    6
    >>> cd.has_duplicates
    True
    >>> cd.has_repeating
    False
    >>> del cd[0]
    >>> Candidate([Char("a")]) == Candidate([Char("a")])
    True
    >>> Candidate([Char("a")]) == Candidate([Char("b")])
    False
    >>> Candidate([Char("a")]) == Char("a")
    False
    """

    __slots__ = ("_text",)

    @deal.pure
    def __init__(self, /, text: list[Slot]) -> None:
        """Initialize the Candidate object."""
        self._text: list[Slot] = list(text)

    @deal.pure
    def __repr__(self) -> str:
        """Return a representation of the Candidate.

        >>> Candidate([Void()])
        Candidate([Void()])
        >>> Candidate([Char("a"), Void(), Char("b")])
        Candidate([Char('a'), Void(), Char('b')])
        """
        return f"{self.__class__.__name__}({self._text!r})"

    @deal.pure
    def __add__(self, other: object) -> "Candidate":
        """Handle addition operator.

        >>> Candidate([Char("a")]) + Candidate([Char("b")])
        Candidate([Char('a'), Char('b')])
        >>> Candidate([Char("a")]) + Candidate([Void()])
        Candidate([Char('a'), Void()])
        >>> Candidate([Char("a")]) + Candidate([Char(" ")])
        Candidate([Char('a'), Char(' ')])
        """
        if not isinstance(other, Candidate):
            return NotImplemented
        return Candidate(self._text + other._text)

    @deal.pure
    def __eq__(self, other: object) -> bool:
        """Check equality between self and other.

        >>> Candidate([Char("a")]) == Candidate([Char("a")])
        True
        >>> Candidate([Char("a")]) == Candidate([Char("b")])
        False
        >>> Candidate([Char("a")]) == "a"
        False
        """
        if not isinstance(other, Candidate):
            return NotImplemented
        return self._text == other._text

    @deal.pure
    def __hash__(self) -> int:
        """Return a hash of self."""
        return hash(tuple(self._text))

    @deal.pure
    def __len__(self) -> int:
        """Return the length of the string."""
        return len(self._text)

    @deal.pure
    def __str__(self) -> str:
        """Return the plain text of the string.

        >>> str(Candidate([Void(), Void()]))
        '••'
        >>> str(Candidate([Char(" ")]))
        ' '
        >>> str(Candidate([Char("a")]))
        'a'
        >>> str(Candidate([Char("a"), Void()]))
        'a•'
        """
        return "".join(str(c) for c in self._text)

    @deal.pure
    def __iter__(self) -> Iterator[Slot]:
        """Iterate over the text.

        >>> c = iter(Candidate([Char("a"), Void(), Char("b")]))
        >>> next(c)
        Char('a')
        >>> next(c)
        Void()
        >>> next(c)
        Char('b')
        >>> try:
        ...     next(c)
        ... except StopIteration:
        ...     print("winner")
        winner
        """
        yield from self._text

    @deal.raises(IndexError)
    def __getitem__(self, item: int) -> Slot:
        """Provide subscriptability."""
        return self._text[item]

    @deal.raises(IndexError)
    def __setitem__(self, item: int, value: Slot) -> None:
        """Provide item assignment."""
        self._text[item] = value

    @deal.raises(IndexError)
    def __delitem__(self, item: int) -> None:
        """Provide item deletion."""
        del self._text[item]

    @property
    def voids(self) -> list[int]:
        """Return the open slots.

        >>> Candidate([Char("a"), Void(), Char("b")]).voids
        [1]
        >>> Candidate([Void(), Char("a"), Void(), Char("b"), Void()]).voids
        [0, 2, 4]
        """
        return [
            i for i, item in enumerate(self._text) if isinstance(item, Void)
        ]

    @deal.raises(DumbConstraintError)
    def scatter(
        self, *, count: int, slots: list[str], allow_repeating: bool
    ) -> None:
        """Randomly insert `count` characters from the given charstack.

        Respect the allow_repeating setting.
        """
        for i in range(count):
            char_next: str | None
            char_prev: str | None

            if void_random := secrets.choice(self.voids):
                char_prev = str(self[void_random - 1])
            else:
                char_prev = None
            try:
                char_next = str(self[void_random + 1])
            except IndexError:
                char_next = None

            secrets.SystemRandom().shuffle(slots)
            for char in slots:
                if allow_repeating or char not in (char_prev, char_next):
                    self[void_random] = Char(char)
                    break
            else:
                msg = (
                    f"Failed scattering into {self!s} "
                    f"on iteration {i} of {count}"
                    f"from {sorted(slots)}"
                )
                raise DumbConstraintError(msg)

    @deal.pure
    @deal.post(
        lambda result: result >= 0,
        message="Count cannot be negative.",
    )
    def _count_string_type(self, haystack: list[Slot]) -> int:
        """Count how many characters in the password are part of the haystack.

        >>> cd = Candidate([Void()])
        >>> cd._count_string_type([Char(c) for c in string.ascii_lowercase])
        0
        >>> cd = Candidate([Void(), Void()])
        >>> cd._count_string_type([Char(c) for c in string.ascii_lowercase])
        0
        >>> cd = Candidate(
        ...     [
        ...         Char("!"),
        ...         Char("a"),
        ...         Char("b"),
        ...         Char("c"),
        ...         Char("D"),
        ...         Char("E"),
        ...         Char("F"),
        ...         Char("G"),
        ...         Void(),
        ...         Char("1"),
        ...         Char("2"),
        ...         Char("3"),
        ...         Char("!"),
        ...         Char("a"),
        ...         Char("D"),
        ...         Void(),
        ...     ]
        ... )
        >>> cd._count_string_type([Char(c) for c in string.ascii_lowercase])
        4
        >>> cd._count_string_type([Char(c) for c in string.ascii_uppercase])
        5
        >>> cd._count_string_type([Char(c) for c in string.punctuation])
        2
        >>> cd = Candidate([Char("0"), Char("#"), Char("#")])
        >>> cd._count_string_type([Char(c) for c in string.digits])
        1
        >>> cd._count_string_type([Char(c) for c in string.punctuation])
        2
        """
        return len([slot for slot in self._text if slot in haystack])

    @property
    @deal.pure
    @deal.post(
        lambda result: result >= 0,
        message="Count cannot be negative.",
    )
    def digits(self) -> int:
        """Return a count of the ASCII digit characters in the password.

        >>> Candidate([Void()]).digits
        0
        >>> Candidate([Char("a"), Char("b"), Char("c")]).digits
        0
        >>> Candidate([Char("1"), Char("2"), Char("3")]).digits
        3
        >>> Candidate([Char("0"), Char("a")]).digits
        1
        >>> Candidate([Char("0"), Char("#")]).digits
        1
        """
        return self._count_string_type([Char(c) for c in string.digits])

    @property
    @deal.pure
    @deal.post(
        lambda result: result >= 0,
        message="Count cannot be negative.",
    )
    def specials(self) -> int:
        """Return a count of the ASCII punctuation characters in the password.

        >>> Candidate([Void()]).specials
        0
        >>> Candidate([Char("a"), Char("b"), Char("c")]).specials
        0
        >>> Candidate([Char("a"), Char("%"), Char("%"), Void()]).specials
        2
        >>> Candidate([Char("!"), Void(), Char("!"), Char("c")]).specials
        2
        """
        return self._count_string_type([Char(c) for c in string.punctuation])

    @property
    @deal.pure
    @deal.post(
        lambda result: result >= 0,
        message="Count cannot be negative.",
    )
    def uppers(self) -> int:
        """Return a count of the ASCII uppercase characters in the password.

        >>> Candidate([Void()]).uppers
        0
        >>> Candidate([Char("a"), Char("b"), Char("c")]).uppers
        0
        >>> Candidate([Char("A"), Char("B"), Char("c"), Char("A")]).uppers
        3
        >>> Candidate([Char("A"), Char("B"), Char("C")]).uppers
        3
        """
        return self._count_string_type(
            [Char(c) for c in string.ascii_uppercase]
        )

    @property
    @deal.pure
    @deal.post(
        lambda result: result >= 0,
        message="Count cannot be negative.",
    )
    def lowers(self) -> int:
        """Return a count of the ASCII lowercase characters in the password.

        >>> Candidate([Void()]).lowers
        0
        >>> Candidate([Char("a"), Char("b"), Char("c"), Char("a")]).lowers
        4
        >>> Candidate([Char("A"), Char("B"), Char("c"), Char("A")]).lowers
        1
        >>> Candidate([Char("A"), Char("B"), Char("C")]).lowers
        0
        """
        return self._count_string_type(
            [Char(c) for c in string.ascii_lowercase]
        )

    @property
    @deal.pure
    def has_duplicates(self) -> bool:
        """Return if the password has duplicate characters.

        >>> Candidate([Void()]).has_duplicates
        False
        >>> Candidate([Char("A"), Char("B"), Char("C")]).has_duplicates
        False
        >>> Candidate([Char("A"), Char("B"), Char("A")]).has_duplicates
        True
        >>> Candidate([Char("A"), Char("B"), Char("B")]).has_duplicates
        True
        """
        return len(set(self._text)) != len(self._text) if self._text else False

    @property
    @deal.pure
    def has_repeating(self) -> bool:
        """Return if the password has repeating characters.

        >>> Candidate([]).has_repeating
        False
        >>> Candidate([Void()]).has_repeating
        False
        >>> Candidate([Void(), Void()]).has_repeating
        False
        >>> Candidate([Char("A")]).has_repeating
        False
        >>> Candidate([Char("A"), Char("B"), Char("A")]).has_repeating
        False
        >>> Candidate([Char("A"), Char("A"), Char("B")]).has_repeating
        True
        >>> Candidate([Char("A"), Char("B"), Char("B")]).has_repeating
        True
        >>> Candidate([Char("A"), Char("B"), Char("A")]).has_repeating
        False
        """
        return any(
            self._text[i] == self._text[i - 1]
            for i in range(1, len(self._text))
            if not isinstance(self._text[i], Void)
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
    def extend(self, slots: Iterator[Slot]) -> None:
        """Extend the password by taking values from an iterator.

        >>> cd = Candidate([Void()])
        >>> cd.extend([Char("a"), Char("b"), Char("c")])
        >>> cd._text
        [Void(), Char('a'), Char('b'), Char('c')]
        >>> cd = Candidate([Char("1"), Char("2"), Char("3")])
        >>> cd.extend([Char("a"), Char(" "), Char("c")])
        >>> cd._text
        [Char('1'), Char('2'), Char('3'), Char('a'), Char(' '), Char('c')]
        """
        self._text.extend(slots)
