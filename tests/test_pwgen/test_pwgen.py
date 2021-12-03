import deal

import dumbpw.pwgen as pwgen

test_generate = deal.cases(pwgen._generate)

# @deal.cases(pwgen._generate)
# def test_generate(case: deal.TestCase) -> None:
#     case()
