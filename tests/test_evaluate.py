import pytest

from math import *
from app.evaluate import evaluate

VALUES = [1, 2, 4]


def generate_test_cases(expression, py_expression, values):
    return [(expression, value, py_expression(value)) for value in values]


@pytest.mark.parametrize(
    "expression, value, expected",
    generate_test_cases("sin(x+1)*x^2", lambda x: sin(x + 1) * x ** 2, VALUES),
)
def test_evaluate(expression, value, expected):
    assert evaluate(expression, value) == expected
