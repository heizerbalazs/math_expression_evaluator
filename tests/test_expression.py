import pytest

from operator import add, sub, mul, truediv, mod, pow, gt, eq, lt

# from math import sin, cos, tan, log, exp
from itertools import product

from app.expression import AlgebraicExpression, Constant, Operation


@pytest.mark.parametrize(
    "expression, result",
    [
        (AlgebraicExpression(None, Constant(3), Constant(2), Operation("+")), 5),
        (AlgebraicExpression(None, Constant(3), Constant(2), Operation("-")), 1),
        (AlgebraicExpression(None, Constant(3), Constant(2), Operation("*")), 6),
        (
            AlgebraicExpression(None, Constant(3), Constant(2), Operation("/")),
            1.5,
        ),
        (AlgebraicExpression(None, Constant(3), Constant(2), Operation("%")), 1),
        (AlgebraicExpression(None, Constant(3), Constant(2), Operation("^")), 9),
        # (2+3)*(4+5) == 45
        (
            AlgebraicExpression(
                None,
                AlgebraicExpression(None, Constant(2), Constant(3), Operation("+")),
                AlgebraicExpression(None, Constant(4), Constant(5), Operation("+")),
                Operation("*"),
            ),
            45,
        ),
        # 2+(3*4)+5 == 19
        (
            AlgebraicExpression(
                None,
                Constant(2),
                AlgebraicExpression(
                    None,
                    AlgebraicExpression(None, Constant(3), Constant(4), Operation("*")),
                    Constant(5),
                    Operation("+"),
                ),
                Operation("+"),
            ),
            19,
        ),
    ],
)
def test_algebraic_expression(expression, result):
    assert expression.evaluate(at={}) == result


@pytest.mark.parametrize("value", [0, 1, 3.1415, -4, -0.5, 12321432, -2131413411])
def test_constant(value):
    c = Constant(value)
    assert c.evaluate(at={}) == value


@pytest.mark.parametrize(
    "symbol, expected_priority, expected_operator",
    [
        ("+", 0, add),
        ("-", 0, sub),
        ("*", 1, mul),
        ("/", 1, truediv),
        ("%", 1, mod),
        ("^", 2, pow),
    ],
)
def test_operation(symbol, expected_priority, expected_operator):
    o = Operation(symbol)
    assert o.priority == expected_priority
    assert o.operator == expected_operator


case_sets = [
    (["+", "-"], ["+", "-"], [eq]),
    (["*", "/", "%"], ["*", "/", "%"], [eq]),
    (["^"], ["^"], [eq]),
    (["+", "-"], ["*", "/", "%", "^"], [lt]),
    (["*", "/", "%"], ["^"], [lt]),
    (["^"], ["+", "-", "*", "/", "%"], [gt]),
    (["*", "/", "%"], ["+", "-"], [gt]),
]


@pytest.mark.parametrize(
    "symbol1, symbol2, comparison",
    [case for case_set in case_sets for case in product(*case_set)],
)
def test_operation_order(symbol1, symbol2, comparison):
    o1 = Operation(symbol1)
    o2 = Operation(symbol2)
    assert comparison(o1, o2)
