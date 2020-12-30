from string import ascii_lowercase, digits
from typing import Dict

from app.expression import (
    AlgebraicExpression,
    Operation,
    Constant,
    FunctionOperation,
    Variable,
)


def is_letter(c):
    return c in ascii_lowercase


def is_digit(c):
    return c in digits


def is_operaton(c):
    return c in Operation.operations.keys()


def is_variable(c, variables):
    return c in variables.keys()


def find_last_letter(expression, start):
    i = start + 1
    n = len(expression)
    while i < n:
        if expression[i] in ascii_lowercase:
            i += 1
        else:
            return start, i
    return start, n


def find_last_digit(expression, start):
    decimal_points = 0
    i = start + 1
    n = len(expression)
    while i < n:
        if is_digit(expression[i]):
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
                raise Exception(f"Whole number can't start with 0 except 0 at {start}")
            return start, i
    return start, n


def find_closing_parenthesis(expression, start):
    lvl = 1
    i = start + 1
    n = len(expression)
    while i < n:
        if expression[i] == "(":
            lvl += 1
        elif expression[i] == ")":
            lvl -= 1

        if lvl == 0:
            return start, i + 1
        i += 1


def expression_tree_builder(
    expression: str,
    variables: Dict,
    expression_tree: AlgebraicExpression = AlgebraicExpression(),
    index: int = 0,
):
    n = len(expression)
    if index < n:
        c = expression[index]
        # handling parentheses
        if c == "(":
            start, end = find_closing_parenthesis(expression, index)
            _, sub_expression = expression_tree_builder(
                expression[start:end], variables, AlgebraicExpression(), 1
            )
            index = end - 1
            if expression_tree.lhs is None:
                expression_tree.lhs = sub_expression
            else:
                expression_tree.rhs = sub_expression
        elif c == ")":
            if expression_tree.rhs is None:
                expression_tree.rhs = Constant(0)
        # handling letters
        elif is_letter(c):
            if is_variable(c, variables):
                variable = Variable(c, variables)
                if expression_tree.lhs is None:
                    expression_tree.lhs = variable
                else:
                    expression_tree.rhs = variable
            else:
                start, end = find_last_letter(expression, index)
                sub_expression = AlgebraicExpression()
                sub_expression.function = FunctionOperation(expression[start:end])
                index = end
                start, end = find_closing_parenthesis(expression, index)
                _, sub_expression = expression_tree_builder(
                    expression[start:end], variables, sub_expression, 1
                )
                index = end - 1
                if expression_tree.lhs is None:
                    expression_tree.lhs = sub_expression
                else:
                    expression_tree.rhs = sub_expression
        # handling digits
        elif is_digit(c):
            start, end = find_last_digit(expression, index)
            value = float(expression[start:end])
            index = end - 1
            if expression_tree.lhs is None:
                expression_tree.lhs = Constant(value)
            else:
                expression_tree.rhs = Constant(value)
        # handling operations
        elif is_operaton(c):
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
                index, expression_tree.rhs = expression_tree_builder(
                    expression, variables, sub_expression, index
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

        return expression_tree_builder(
            expression, variables, expression_tree, index + 1
        )
    else:
        if expression_tree.rhs is None:
            expression_tree.rhs = Constant(0)
        return index, expression_tree
