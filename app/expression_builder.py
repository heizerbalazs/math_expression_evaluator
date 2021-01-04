from string import ascii_lowercase, digits
from typing import Dict

from app.expression import (
    AlgebraicExpression,
    Operation,
    Constant,
    FunctionOperation,
    Variable,
)


class ExpressionTreeBuilder:
    def __init__(self, expression, variables):
        self.expression = expression
        self.expression_end = len(expression)
        self.variables = variables

    @staticmethod
    def is_letter(c):
        return c in ascii_lowercase

    @staticmethod
    def is_digit(c):
        return c in digits

    @staticmethod
    def is_operaton(c):
        return c in Operation.operations.keys()

    @staticmethod
    def is_variable(c, variables):
        return c in variables.keys()

    @staticmethod
    def find_last_letter(expression, start):
        i = start + 1
        end = len(expression)
        while i < end:
            if expression[i] in ascii_lowercase:
                i += 1
            else:
                return start, i
        return start, end

    @staticmethod
    def find_last_digit(expression, start):
        decimal_points = 0
        i = start + 1
        end = len(expression)
        while i < end:
            if ExpressionTreeBuilder.is_digit(expression[i]):
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
    def find_closing_parenthesis(expression, start):
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

    def parse_expression(
        self,
        expression_tree: AlgebraicExpression,
        index: int,
        end: int,
    ):
        expression = self.expression
        variables = self.variables
        if end == 0:
            end = self.expression_end

        if index < end:
            c = expression[index]
            # handling parentheses
            if c == "(":
                _start, _end = ExpressionTreeBuilder.find_closing_parenthesis(
                    expression, index
                )
                _, sub_expression = self.parse_expression(
                    AlgebraicExpression(), _start + 1, _end
                )
                index = _end - 1
                if expression_tree.lhs is None:
                    expression_tree.lhs = sub_expression
                else:
                    expression_tree.rhs = sub_expression
            elif c == ")":
                if expression_tree.rhs is None:
                    expression_tree.rhs = Constant(0)
            # handling letters
            elif ExpressionTreeBuilder.is_letter(c):
                if ExpressionTreeBuilder.is_variable(c, variables):
                    variable = Variable(c, variables)
                    if expression_tree.lhs is None:
                        expression_tree.lhs = variable
                    else:
                        expression_tree.rhs = variable
                else:
                    _start, _end = ExpressionTreeBuilder.find_last_letter(
                        expression, index
                    )
                    sub_expression = AlgebraicExpression()
                    sub_expression.function = FunctionOperation(expression[_start:_end])
                    index = _end
                    _start, _end = ExpressionTreeBuilder.find_closing_parenthesis(
                        expression, index
                    )
                    _, sub_expression = self.parse_expression(
                        sub_expression, _start + 1, _end
                    )
                    index = _end - 1
                    if expression_tree.lhs is None:
                        expression_tree.lhs = sub_expression
                    else:
                        expression_tree.rhs = sub_expression
            # handling digits
            elif ExpressionTreeBuilder.is_digit(c):
                _start, _end = ExpressionTreeBuilder.find_last_digit(expression, index)
                value = float(expression[_start:_end])
                index = _end - 1
                if expression_tree.lhs is None:
                    expression_tree.lhs = Constant(value)
                else:
                    expression_tree.rhs = Constant(value)
            # handling operations
            elif ExpressionTreeBuilder.is_operaton(c):
                new_operation = Operation(c)
                if expression_tree.lhs is None:
                    expression_tree.lhs = Constant(0)
                    expression_tree.operation = new_operation
                elif expression_tree.rhs is None:
                    expression_tree.operation = new_operation
                elif (
                    expression_tree.operation < new_operation
                ) | new_operation.has_top_priority():
                    sub_expression = AlgebraicExpression()
                    sub_expression.lhs = expression_tree.rhs
                    index, expression_tree.rhs = self.parse_expression(
                        sub_expression, index, end
                    )
                else:
                    expression_tree.lhs = AlgebraicExpression(
                        expression_tree.lhs,
                        expression_tree.rhs,
                        expression_tree.operation,
                        expression_tree.function,
                    )
                    expression_tree.rhs = None
                    expression_tree.operation = new_operation

            return self.parse_expression(expression_tree, index + 1, end)
        else:
            if expression_tree.rhs is None:
                expression_tree.rhs = Constant(0)
            return index, expression_tree
