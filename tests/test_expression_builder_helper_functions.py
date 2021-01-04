import pytest

from app.expression_builder import ExpressionTreeBuilder


def test_find_last_letter():
    pass


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("0+", 0.0),
        ("3.1415+", 3.1415),
        ("123+", 123.0),
        ("328.14+", 328.14),
        ("10.+", 10.0),
    ],
)
def test_find_last_digit(expression, expected):
    start, end = ExpressionTreeBuilder.find_last_digit(expression, 0)
    assert float(expression[start:end]) == expected


@pytest.mark.parametrize(
    "expression, expected",
    [
        ("0123+", 0),
        ("01.23+", 1.23),
        ("1231321.23534654.32131+", 1.23),
    ],
)
def test_find_last_digit_exception(expression, expected):
    with pytest.raises(Exception):
        start, end = find_last_digit(expression, 0)
        assert float(expression[start:end]) == expected


def test_find_last_parentheses():
    pass