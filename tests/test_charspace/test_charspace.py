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
def test_blocklist(text):
    sp = Charspace(blocklist=text)

    assert all(char not in text for char in sp.charset)
