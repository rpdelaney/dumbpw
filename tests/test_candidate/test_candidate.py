import sys

import hypothesis.strategies as strats
from hypothesis import given

from dumbpw.candidate import Candidate


def test_candidate_zero_len_duplicates():
    cd = Candidate("")

    assert not cd.has_duplicates


@given(strats.text(min_size=1))
def test_candidate_has_duplicates(text):
    cd = Candidate(text + text)

    assert cd.has_duplicates


@given(strats.text(min_size=1))
def test_candidate_has_no_duplicates(text):
    cd = Candidate("".join(set(text)))

    assert not cd.has_duplicates


def test_candidate_zero_len_repeating():
    cd = Candidate("")

    assert not cd.has_repeating


@given(strats.text(min_size=1))
def test_candidate_has_repeating(text):
    cd = Candidate(sorted(text + text))

    assert cd.has_repeating


@given(strats.text(min_size=1))
def test_candidate_has_no_repeating(text):
    cd = Candidate(
        "".join(set(text)),
    )

    assert not cd.has_repeating


@given(strats.text())
def test_candidate_copy_method(text):
    cd = Candidate(text)
    cp = cd.copy()

    assert cd == cp
    assert cd is not cp


@given(strats.text())
def test_candidate_addable(text):
    """Candidate can be added with a string."""
    cd = Candidate(text)

    cd += "a"

    assert str(cd) == text + "a"


@given(strats.text())
def test_candidate_stringifiable(text):
    """Candidate can be coerced to a string."""
    cd = Candidate(text)

    assert str(cd) == text


@given(strats.text(min_size=1))
def test_candidate_subscriptable(text):
    """Candidate is subscriptable."""
    cd = Candidate(text)

    assert cd[0] == text[0]


@given(strats.text())
def test_candidate_hashable(text):
    """Candidate is hashable."""
    cd = Candidate(text)

    assert hash(cd) is not None


@given(strats.text())
def test_candidate_sizable(text):
    """Candidate is sizable."""
    cd = Candidate(text)

    assert sys.getsizeof(cd) is not None
