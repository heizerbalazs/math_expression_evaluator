import pytest

from app.expression import check_parentheses, check_type


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("sin(x", False),
        ("x+1)", False),
        ("(x+1)^2", True),
        ("sin(x)*2)", False),
        ("(x+3)*(x+4)", True),
        ("sin(3*(x+1))", True),
        ("(sin(x)+cos(x))^2", True),
        ("(()())(", False),
        ("(()()))", False),
        ("(()())()", True),
    ],
)
def test_check_parentheses(expression, expected):
    assert check_parentheses(expression) == expected


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("sin(x)", "function"),
        ("cos(x+1)", "function"),
        ("tan(3*(x+1))", "function"),
        ("exp((x+1)*(x+3))", "function"),
        ("log(x-1)", "function"),
        ("x+3", "expression"),
        ("sin(x)^2+cos(x)^2", "expression"),
        ("sin(x)^cos(x)", "expression"),
        ("x+sin(x)", "expression"),
        ("sin(x)*x^2", "expression"),
        ("x", "variable"),
        ("0", "constant"),
        ("1", "constant"),
        ("3.14", "constant"),
        ("314", "constant"),
    ],
)
def test_check_type(expression, expected):
    assert check_type(expression) == expected