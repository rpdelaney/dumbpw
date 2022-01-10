import deal

import dumbpw.pwgen as pwgen


@deal.cases(
    func=pwgen.generate,
)
def test_generate(case: deal.TestCase) -> None:
    case()


@deal.cases(
    func=pwgen.search,
)
def test_search(case: deal.TestCase) -> None:
    case()
