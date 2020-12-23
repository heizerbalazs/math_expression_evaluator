import pytest

from app.expression_builder import expression_builder


@pytest.mark.parametrize(
    "expression, expected_result",
    [("(2*3+4)*5", 50), ("(2+3)*(4+5)", 45), ("2+(3*4)+5", 19)],
)
def test_expression_builder(expression, expected_result):
    expr = expression_builder(expression)
    assert expr.evaluate() == expected_result