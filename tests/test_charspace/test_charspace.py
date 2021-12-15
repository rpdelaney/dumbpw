from collections import Counter

import hypothesis.strategies as strats
from hypothesis import given

from dumbpw.charspace import Charspace


def test_defaults():
    sp = Charspace()
    result = "".join(sorted(sp.charset))
    expected = (
        """!#$%&()*+,-./0123456789:<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ"""
        """[]^_`abcdefghijklmnopqrstuvwxyz{|}~"""
    )

    assert result == expected


@given(strats.text())
def test_blocklist(text):
    """The charset must not contain any characters from the blocklist."""
    sp = Charspace(blocklist=text)

    assert all(char not in text for char in sp.charset)


def test_charset_unique():
    """The characters in the charset must be deduplicated."""
    sp = Charspace()
    count = Counter()

    for c in sp.charset:
        count.update(c)

    assert all(value == 1 for _, value in count.items())


def test_base_charset():
    """The characters in the base charspace must come from the charset
    properties."""
    sp = Charspace()

    assert any(
        char in sp.extras
        or char in sp.uppers
        or char in sp.lowers
        or char in sp.digits
        for char in sp.base_charset
    )


def test_dict():
    sp = Charspace()

    assert dict(sp)
