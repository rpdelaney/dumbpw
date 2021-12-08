import deal

import dumbpw.pwgen as pwgen


@deal.cases(
    func=pwgen.generate,
)
def test_generate(case: deal.TestCase) -> None:
    case()
