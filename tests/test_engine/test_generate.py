import deal

from dumbpw.engine import generate


@deal.cases(
    func=generate,
)
def test_generate(case: deal.TestCase) -> None:
    case()
