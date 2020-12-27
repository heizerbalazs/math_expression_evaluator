import pytest

from app.expression_builder import expression_tree_builder
from app.expression import AlgebraicExpression


@pytest.mark.parametrize(
    "expression, expected_result",
    [
        ("2+3", 5),
        ("2+3+4", 9),
        ("1+2+3+4+5+6+7+8+9", 45),
        ("1-2+3+4+5+6+7+8+9", 41),
        ("1-2+3-4+5-6+7-8+9", 5),
        (
            "1+2^3*4-5+6/7",
            1 + 2 ** 3 * 4 - 5 + 6 / 7,
        ),
        ("2*3*4/5", ((2 * 3) * 4) / 5),
        ("2/3*4/5", 2 / 3 * 4 / 5),
        ("2*3+4", 10),
        ("2^3+4", 12),
        ("2+3*4", 14),
        ("2+3^4", 83),
        ("2-3", -1),
        ("2*3", 6),
        ("2/3", 2 / 3),
        ("2%3", 2 % 3),
        ("2^3", 2 ** 3),
    ],
)
def test_expression_tree_builder(expression, expected_result):
    _, expr = expression_tree_builder(expression, AlgebraicExpression(), 0)
    assert expr.evaluate() == expected_result