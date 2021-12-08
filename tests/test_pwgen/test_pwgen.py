import string

import deal
from hypothesis.strategies import frozensets, sampled_from

import dumbpw.pwgen as pwgen


@deal.cases(
    func=pwgen.generate,
    kwargs={
        "keyspace": frozensets(sampled_from(string.printable)),
    },
)
def test_generate(case: deal.TestCase) -> None:
    case()
