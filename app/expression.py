from operator import add, sub, mul, truediv, mod, pow
from math import sin, cos, tan, log, exp
from abc import ABC, abstractmethod


class Expression(ABC):
    @abstractmethod
    def evaluate(self):
        pass


class AlgebraicExpression(Expression):
    def __init__(
        self,
        lhs,
        rhs,
        operation,
        function=lambda x: x,
    ):
        self.lhs = lhs
        self.rhs = rhs
        self.operation = operation
        self.function = function

    def evaluate(self):
        lhs = self.lhs if type(self.lhs) == float else self.lhs.evaluate()
        rhs = self.rhs if type(self.rhs) == float else self.rhs.evaluate()
        arg = self.operation.operator(lhs, rhs)
        value = self.function(arg)
        return value


class Constant(Expression):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value


class Operation:

    prioroties = {
        "+": [0, add],
        "-": [0, sub],
        "*": [1, mul],
        "/": [1, truediv],
        "%": [1, mod],
        "^": [2, pow],
    }

    def __init__(self, symbol):
        if symbol not in Operation.prioroties.keys():
            raise Exception(f"{symbol} is not a valid operator.")

        self.symbol = symbol
        self.priority, self.operator = Operation.prioroties[symbol]

    def __eq__(self, other):
        return self.priority == other.priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __lt__(self, other):
        return self.priority < other.priority
