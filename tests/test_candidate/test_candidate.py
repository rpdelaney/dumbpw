import hypothesis.strategies as strats
from hypothesis import given

from dumbpw.candidate import Candidate


def test_zero_len_duplicates():
    cd = Candidate("")

    assert not cd.has_duplicates


@given(strats.text(min_size=1))
def test_has_duplicates(text):
    cd = Candidate(text + text)

    assert cd.has_duplicates


@given(strats.text(min_size=1))
def test_has_no_duplicates(text):
    cd = Candidate("".join(set(text)))

    assert not cd.has_duplicates


def test_zero_len_repeating():
    cd = Candidate("")

    assert not cd.has_repeating


@given(strats.text(min_size=1))
def test_has_repeating(text):
    cd = Candidate(sorted(text + text))

    assert cd.has_repeating


@given(strats.text(min_size=1))
def test_has_no_repeating(text):
    cd = Candidate(
        "".join(set(text)),
    )

    assert not cd.has_repeating


@given(strats.text())
def test_len(text):
    cd = Candidate(text)

    assert len(cd) == len(text)


@given(strats.text())
def test_str(text):
    cd = Candidate(text)

    assert str(cd) == text


@given(strats.text())
def test_repr(text):
    cd = Candidate(text)

    assert repr(cd) == f'dumbpw.candidate.Candidate("{text}")'
