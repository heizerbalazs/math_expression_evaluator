from app.expression import AlgebraicExpression, Operation, Constant

digits = list(map(lambda x: str(x), [i for i in range(10)]))


def is_digit(c):
    return c in digits


def is_operaton(c):
    return c not in digits


def find_end(expression, start):
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
            if expression_tree.lhs is None:
                start, end = find_end(expression, index)
                index, expression_tree.lhs = expression_tree_builder(
                    expression[start:end], AlgebraicExpression(), 1
                )
                index = end
            else:
                start, end = find_end(expression, index)
                index, expression_tree.rhs = expression_tree_builder(
                    expression[start:end], AlgebraicExpression(), 1
                )
                index = end
        elif c == ")":
            return expression_tree_builder(expression, expression_tree, index + 1)
        # handling digits
        elif is_digit(c) & (expression_tree.lhs is not None):
            expression_tree.rhs = Constant(float(c))
        elif is_digit(c) & (expression_tree.lhs is None):
            expression_tree.lhs = Constant(float(c))
        # handling operations
        elif is_operaton(c):
            new_operation = Operation(c)
            if expression_tree.lhs is None:
                expression_tree.lhs = Constant(0)
                expression_tree.operation = new_operation
            elif expression_tree.rhs is None:
                expression_tree.operation = new_operation
            else:
                if (expression_tree.operation < new_operation) | (c == "^"):
                    exp = AlgebraicExpression()
                    exp.lhs = Constant(expression_tree.rhs.evaluate())
                    index, expression_tree.rhs = expression_tree_builder(
                        expression, exp, index
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
