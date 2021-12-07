import deal

import dumbpw.pwgen as pwgen


@deal.cases(func=pwgen._generate)
def test_generate(case: deal.TestCase) -> None:
    case()
