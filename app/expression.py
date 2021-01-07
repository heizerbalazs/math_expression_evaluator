from operator import add, sub, mul, truediv, mod, pow
from math import sin, cos, tan, log, exp
from abc import ABC, abstractmethod
from typing import Dict


class Operation:
    operations = {
        "+": [0, add],
        "-": [0, sub],
        "*": [1, mul],
        "/": [1, truediv],
        "%": [1, mod],
        "^": [2, pow],
    }

    def __init__(self, symbol: str = "+"):
        if symbol not in Operation.operations.keys():
            raise Exception(f"{symbol} is not a valid operator.")

        self.priority, self.operator = Operation.operations[symbol]

    def __eq__(self, other):
        return self.priority == other.priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __ge__(self, other):
        return self.priority >= other.priority

    def __lt__(self, other):
        return self.priority < other.priority

    def __le__(self, other):
        return self.priority <= other.priority

    def has_top_priority(self):
        max_priority = max(
            [operation[0] for operation in Operation.operations.values()]
        )
        return self.priority == max_priority


class FunctionOperation:
    functions = {
        "": lambda x: x,
        "sin": sin,
        "cos": cos,
        "tan": tan,
        "cot": lambda x: 1 / tan(x),
        "log": log,
        "exp": exp,
    }

    def __init__(self, name: str = ""):
        if name not in FunctionOperation.functions.keys():
            raise Exception(f"{name} is not a valid mathematical function.")

        self.function = FunctionOperation.functions[name]


class Expression(ABC):
    @abstractmethod
    def evaluate(self, at: Dict[str, float]) -> float:
        pass


class AlgebraicExpression(Expression):
    def __init__(
        self,
        lhs: Expression = None,
        rhs: Expression = None,
        operation: Operation = Operation(),
        function: FunctionOperation = FunctionOperation(),
    ):
        self.lhs = lhs
        self.rhs = rhs
        self.operation = operation
        self.function = function

    def evaluate(self, at: Dict[str, float]) -> float:
        lhs = self.lhs.evaluate(at)
        rhs = self.rhs.evaluate(at)
        arg = self.operation.operator(lhs, rhs)
        value = self.function.function(arg)
        return value


class Constant(Expression):
    def __init__(self, value):
        self.value = value

    def evaluate(self, at: Dict[str, float]) -> float:
        return self.value


class Variable(Expression):
    def __init__(self, symbol: str):
        self.symbol = symbol

    def evaluate(self, at: Dict[str, float]) -> float:
        # TODO: refactor evaluate
        return at[self.symbol]


# TODO: replace None with placeholder expression