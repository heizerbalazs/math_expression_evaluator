import copy

from string import ascii_lowercase, digits
from typing import Dict, Tuple

from app.expression import (
    AlgebraicExpression,
    Operation,
    Constant,
    FunctionOperation,
    Variable,
)


class StringProcessor:
    @staticmethod
    def is_letter(c: str) -> bool:
        return c in ascii_lowercase

    @staticmethod
    def is_digit(c: str) -> bool:
        return c in digits

    @staticmethod
    def is_operation(c: str) -> bool:
        return c in Operation.operations.keys()

    @staticmethod
    def is_variable(c: str, variables: Dict[str, float]) -> bool:
        return c in variables.keys()

    @staticmethod
    def find_last_letter(expression: str, start: int) -> Tuple[int, int]:
        i = start + 1
        end = len(expression)
        while i < end:
            if expression[i] in ascii_lowercase:
                i += 1
            else:
                return start, i
        return start, end

    @staticmethod
    def find_last_digit(expression: str, start: int) -> Tuple[int, int]:
        decimal_points = 0
        i = start + 1
        end = len(expression)
        while i < end:
            if StringProcessor.is_digit(expression[i]):
                i += 1
            elif expression[i] == ".":
                if decimal_points >= 1:
                    raise Exception(
                        f"This is too much decimal points in one number at {start}."
                    )
                decimal_points += 1
                i += 1
            else:
                if (
                    (expression[start] == "0")
                    & (expression[start + 1] != ".")
                    & ((i - start) > 1)
                ):
                    raise Exception(
                        f"Whole number can't start with 0 except 0 at {start}"
                    )
                return start, i
        return start, end

    @staticmethod
    def find_closing_parenthesis(expression: str, start: int) -> Tuple[int, int]:
        lvl = 1
        i = start + 1
        end = len(expression)
        while i < end:
            if expression[i] == "(":
                lvl += 1
            elif expression[i] == ")":
                lvl -= 1

            if lvl == 0:
                return start, i + 1
            i += 1
        raise Exception(f"Opening parenthesis at {start} has no closing pair.")


class ExpressionTreeBuilder:
    def __init__(self, expression: str, variables: Dict[str, float]):
        self.expression = expression
        self.expression_end = len(expression)
        self.variables = variables

    def build_expression(self):
        return self.parse_expression(AlgebraicExpression(), 0, -1)

    def parse_expression(
        self, tree: AlgebraicExpression, index: int = 0, end: int = -1
    ) -> Tuple[int, AlgebraicExpression]:
        if end == -1:
            end = self.expression_end

        if index < end:
            c = self.expression[index]
            # handling parentheses
            if c == "(":
                _start, _end = StringProcessor.find_closing_parenthesis(
                    self.expression, index
                )
                _, sub_tree = self.parse_expression(
                    AlgebraicExpression(), _start + 1, _end
                )
                index = _end - 1
                if tree.lhs is None:
                    tree.lhs = sub_tree
                else:
                    tree.rhs = sub_tree
            elif c == ")":
                if tree.rhs is None:
                    tree.rhs = Constant(0)
            # handling letters
            elif StringProcessor.is_letter(c):
                if StringProcessor.is_variable(c, self.variables):
                    variable = Variable(c)
                    if tree.lhs is None:
                        tree.lhs = variable
                    else:
                        tree.rhs = variable
                else:
                    _start, _end = StringProcessor.find_last_letter(
                        self.expression, index
                    )
                    sub_tree = AlgebraicExpression()
                    sub_tree.function = FunctionOperation(self.expression[_start:_end])
                    index = _end
                    _start, _end = StringProcessor.find_closing_parenthesis(
                        self.expression, index
                    )
                    _, sub_tree = self.parse_expression(sub_tree, _start + 1, _end)
                    index = _end - 1
                    if tree.lhs is None:
                        tree.lhs = sub_tree
                    else:
                        tree.rhs = sub_tree
            # handling digits
            elif StringProcessor.is_digit(c):
                _start, _end = StringProcessor.find_last_digit(self.expression, index)
                value = float(self.expression[_start:_end])
                index = _end - 1
                if tree.lhs is None:
                    tree.lhs = Constant(value)
                else:
                    tree.rhs = Constant(value)
            # handling operations
            elif StringProcessor.is_operation(c):
                new_operation = Operation(c)
                if tree.lhs is None:
                    tree.lhs = Constant(0)
                    tree.operation = new_operation
                elif tree.rhs is None:
                    tree.operation = new_operation
                elif (
                    tree.operation < new_operation
                ) | new_operation.has_top_priority():
                    sub_tree = AlgebraicExpression()
                    sub_tree.lhs = tree.rhs
                    index, tree.rhs = self.parse_expression(sub_tree, index, end)
                else:
                    tree.lhs = copy.copy(tree)
                    tree.rhs = None
                    tree.operation = new_operation

            return self.parse_expression(tree, index + 1, end)
        else:
            if tree.rhs is None:
                tree.rhs = Constant(0)
            return index, tree
