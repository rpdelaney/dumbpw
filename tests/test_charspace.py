from collections import Counter

import hypothesis.strategies as strats
from hypothesis import given

from dumbpw.charspace import Charspace


def test_defaults():
    sp = Charspace()
    result = "".join(sorted(sp.charset))
    expected = (
        """!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ"""
        """[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"""
    )

    assert result == expected


@given(strats.text())
def test_blocklist(blocklist):
    """Charset does not contain any characters from the blocklist."""
    sp = Charspace(blocklist=blocklist)

    assert all(char not in sp.charset for char in blocklist)


def test_charset_unique():
    """The characters in the charset are deduplicated."""
    sp = Charspace()
    count = Counter(sp.charset)

    assert all(value == 1 for _, value in count.items())


def test_base_charset():
    """Characters in the base charspace come from the charset properties."""
    sp = Charspace()

    assert any(
        char in sp.extras
        or char in sp.uppers
        or char in sp.lowers
        or char in sp.digits
        for char in sp.base_charset
    )
