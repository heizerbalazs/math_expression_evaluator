import pytest

from math import sin, cos, tan, log, exp

from app.expression_builder import ExpressionTreeBuilder


@pytest.mark.parametrize(
    "expression, expected_result",
    [
        ("2+3", 5),
        ("2+3+4", 9),
        ("2+3*4", 2 + 3 * 4),
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
        ("2*3/4*5", ((2 * 3) / 4) * 5),
        ("2*3/4^2*5", ((2 * 3) / 4 ** 2) * 5),
        ("2/3*4/5", 2 / 3 * 4 / 5),
        ("2*3+4", 10),
        ("2^3+4", 12),
        ("4*3^2-1", 35),
        ("2+4*3^2*5-1", 2 + 4 * 3 ** 2 * 5 - 1),
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
    _, expr = ExpressionTreeBuilder(expression, {}).build_expression()
    assert expr.evaluate(at={}) == float(expected_result)


@pytest.mark.parametrize(
    "expression, expected_result",
    [
        ("2*(2+3)", 10),
        ("(1+2)*3", 9),
        ("2^(3+4*(2+1))", 32768),
        ("2^(3+4*(2+1))+1", 32769),
        ("2^(3+4*(2+1))*5", 32768 * 5),
        (
            "2^(3+4*(2+1)^(2*(1+2)-5))*5",
            32768 * 5,
        ),
        ("((3+2)*4)^((3-2)*3)", ((3 + 2) * 4) ** ((3 - 2) * 3)),
        ("(3+4*(2+1))*4", 60),
        ("4^(3^(2^(1)))", 262144),
        ("4^3^2^1", 262144),
        ("(((5^4)^3)^2)^1", 59604644775390625),
    ],
)
def test_expression_tree_builder_with_parenthases(expression, expected_result):
    _, expr = ExpressionTreeBuilder(expression, {}).build_expression()
    assert expr.evaluate(at={}) == float(expected_result)


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
        ("3.14^2+6.25^3", 3.14 ** 2 + 6.25 ** 3),
        ("(3.14-10)^2+6.25^3", (3.14 - 10) ** 2 + 6.25 ** 3),
        ("-(-3)", -(-3)),
        ("--3", -(-3)),
        (".3+1", 0.3 + 1),
    ],
)
def test_expression_tree_builder_for_floats(expression, expected_result):
    _, expr = ExpressionTreeBuilder(expression, {}).build_expression()
    assert expr.evaluate(at={}) == float(expected_result)


@pytest.mark.parametrize(
    "expression, expected_result",
    [
        ("sin(3.14)", sin(3.14)),
        ("cos(3.14)", cos(3.14)),
        ("tan(3.14)", tan(3.14)),
        ("cot(3.14)", 1 / tan(3.14)),
        ("exp(3.14)", exp(3.14)),
        ("log(3.14)", log(3.14)),
        ("sin(3.14+1)", sin(3.14 + 1)),
        ("sin(3.14)^2", sin(3.14) ** 2),
        ("sin(3.14)^2+cos(3.14)^2", sin(3.14) ** 2 + cos(3.14) ** 2),
        ("sin(3.14)*2+cos(3.14)*2", sin(3.14) * 2 + cos(3.14) * 2),
        ("2*sin(3.14+1)+2*cos(3.14+1)", 2 * sin(3.14 + 1) + 2 * cos(3.14 + 1)),
        ("sin(3.14+cos(3.14))", sin(3.14 + cos(3.14))),
        ("log(exp(3.14)+100)", log(exp(3.14) + 100)),
        ("log((3.14+1.3543)*100)", log((3.14 + 1.3543) * 100)),
    ],
)
def test_expression_tree_builder_with_functions(expression, expected_result):
    _, expr = ExpressionTreeBuilder(expression, {}).build_expression()
    assert expr.evaluate(at={}) == float(expected_result)


@pytest.mark.parametrize(
    "expression, variables, expected_result",
    [
        ("x", {"x": 3.14}, 3.14),
        ("x^2", {"x": 3.14}, 3.14 ** 2),
        ("sin(x^2)", {"x": 3.14}, sin(3.14 ** 2)),
        ("sin(x)^2+cos(x)^2", {"x": 3.14}, sin(3.14) ** 2 + cos(3.14) ** 2),
        ("sin(x)^2+cos(y)^2", {"x": 3.14, "y": 2.71}, sin(3.14) ** 2 + cos(2.71) ** 2),
        ("sin(x+1)*x^2", {"x": 4, "y": 2.71}, sin(4 + 1) * 4 ** 2),
        ("sin(x+1)*x^2-3.1", {"x": 4, "y": 2.71}, sin(4 + 1) * 4 ** 2 - 3.1),
        (
            "sin(x+1)*x^2-x^2*sin(x+1)",
            {"x": 4, "y": 2.71},
            sin(4 + 1) * 4 ** 2 - 4 ** 2 * sin(4 + 1),
        ),
        (
            "sin(x+1)*x^2+x^2*sin(x+1)",
            {"x": 4, "y": 2.71},
            sin(4 + 1) * 4 ** 2 + 4 ** 2 * sin(4 + 1),
        ),
        (
            "sin(x+1)*x^2/x^2*sin(x+1)",
            {"x": 4, "y": 2.71},
            sin(4 + 1) * 4 ** 2 / 4 ** 2 * sin(4 + 1),
        ),
        ("sin(x+1)*x^2+3.1", {"x": 4, "y": 2.71}, sin(4 + 1) * 4 ** 2 + 3.1),
        ("x*(x+1)", {"x": 4}, 4 * (4 + 1)),
        ("x*(x+1)", {"x": 5}, 5 * (5 + 1)),
        ("x*(x+1)", {"x": 6}, 6 * (6 + 1)),
        ("x*(x+1)+(1.2-0.3)", {"x": 6}, 6 * (6 + 1) + (1.2 - 0.3)),
    ],
)
def test_expression_tree_builder_with_variables(expression, variables, expected_result):
    _, expr = ExpressionTreeBuilder(expression, variables).build_expression()
    assert expr.evaluate(at=variables) == float(expected_result)


@pytest.mark.parametrize(
    "expression, variables",
    [
        ("xx", {"x": 6}),
        ("0.000.12", {}),
        ("+-3", {}),
        ("+", {}),
        ("()", {}),
        ("(0))", {}),
        ("((0)", {}),
        ("()0", {}),
        ("()1", {}),
        ("sinx", {"x": 6}),
        ("log(2+sinx)", {"x": 6}),
        (")x(", {"x": 6}),
        ("-3x", {"x": 6}),
        ("x/0", {"x": 6}),
    ],
)
def test_expression_tree_builder_for_incorrect_expression(expression, variables):
    with pytest.raises(Exception):
        _, expr = ExpressionTreeBuilder(expression, variables).build_expression()
        expr.evaluate(at=variables)
