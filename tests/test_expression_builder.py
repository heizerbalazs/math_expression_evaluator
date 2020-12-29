import pytest

from app.expression_builder import expression_tree_builder
from app.expression import AlgebraicExpression


@pytest.mark.parametrize(
    "expression, expected_result",
    [
        ("2+3", 5),
        ("2+3+4", 9),
        ("1+2+3+4+5+6+7+8+9", 45),
        ("-1+2+3+4+5+6+7+8+9", 43),
        ("-1-2-3-4-5-6-7-8-9", -45),
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
        ("2^3+1", 2 ** 3 + 1),
        ("2^3^4", 2 ** 3 ** 4),
    ],
)
def test_expression_tree_builder_for_integers(expression, expected_result):
    _, expr = expression_tree_builder(expression, AlgebraicExpression(), 0)
    assert expr.evaluate() == float(expected_result)


@pytest.mark.parametrize(
    "expression, expected_result",
    [
        ("1*(2+3)", 5),
        ("(1+2)*3", 9),
        ("2^(3+4*(2+1))", 32768),
        ("2^(3+4*(2+1))+1", 32769),
        ("2^(3+4*(2+1))*5", 32768 * 5),
        (
            "2^(3+4*(2+1)^(2*(1+2)-5))*5",
            32768 * 5,
        ),
        ("(3+4*(2+1))*4", 60),
        ("4^(3^(2^(1)))", 262144),
        ("4^3^2^1", 262144),
        ("(((5^4)^3)^2)^1", 59604644775390625),
    ],
)
def test_expression_tree_builder_with_parenthases(expression, expected_result):
    _, expr = expression_tree_builder(expression, AlgebraicExpression(), 0)
    assert expr.evaluate() == float(expected_result)


@pytest.mark.parametrize(
    "expression, expected_result",
    [
        ("1.5*(203+3.14)", 1.5 * (203 + 3.14)),
        ("(13+0.2)*0.0003", (13 + 0.2) * 0.0003),
        ("0.2^(30+4.15*(-0.22+1))", 0.2 ** (30 + 4.15 * (-0.22 + 1))),
        ("23^(3+4*(2+1))+1", 23 ** (3 + 4 * (2 + 1)) + 1),
        ("2^(3+4/(-2+0.1))*5", 2 ** (3 + 4 / (-2 + 0.1)) * 5),
        (
            "2^(3/0.4*(2+1)^(2*(1+2)-5))*5",
            2 ** (3 / 0.4 * (2 + 1) ** (2 * (1 + 2) - 5)) * 5,
        ),
    ],
)
def test_expression_tree_builder_for_floats(expression, expected_result):
    _, expr = expression_tree_builder(expression, AlgebraicExpression(), 0)
    assert expr.evaluate() == float(expected_result)
