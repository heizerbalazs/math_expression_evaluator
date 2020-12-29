from string import ascii_lowercase, digits
from app.expression import AlgebraicExpression, Operation, Constant


def is_letter(c):
    return c in ascii_lowercase


def is_digit(c):
    return c in digits


def is_operaton(c):
    return c not in (digits + ascii_lowercase + "(" + ")")


def find_last_letter(expression, start):
    i = start + 1
    n = len(expression)
    while i < n:
        if expression[i] in ascii_lowercase:
            i += 1
        else:
            return start, i


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
            return start, i
        i += 1


def expression_tree_builder(
    expression: str, expression_tree: AlgebraicExpression, index: int
):
    n = len(expression)
    if index < n:
        c = expression[index]
        # handling parentheses
        if c == "(":
            start, end = find_closing_parenthesis(expression, index)
            _, exp = expression_tree_builder(
                expression[start:end], AlgebraicExpression(), 1
            )
            index = end
            if expression_tree.lhs is None:
                expression_tree.lhs = exp
            else:
                expression_tree.rhs = exp
        # handling letters
        elif is_letter(c):
            pass
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
                    expression, sub_expression, index
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

        return expression_tree_builder(expression, expression_tree, index + 1)
    else:
        if expression_tree.rhs is None:
            return index, expression_tree.lhs
        else:
            return index, expression_tree
