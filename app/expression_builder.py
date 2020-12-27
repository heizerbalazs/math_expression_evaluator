from app.expression import AlgebraicExpression, Operation, Constant

digits = list(map(lambda x: str(x), [i for i in range(10)]))


def is_digit(c):
    return c in digits


def is_operaton(c):
    return c not in digits


def expression_tree_builder(
    expression: str,
    expression_tree: AlgebraicExpression = AlgebraicExpression(),
    i: int = 0,
):
    n = len(expression)
    if i < n:
        c = expression[i]
        if is_digit(c) & (expression_tree.lhs != None):
            expression_tree.rhs = Constant(float(c))
            return expression_tree_builder(expression, expression_tree, i + 1)
        elif is_digit(c) & (expression_tree.lhs == None):
            expression_tree.lhs = Constant(float(c))
            return expression_tree_builder(expression, expression_tree, i + 1)
        elif is_operaton(c):
            new_operation = Operation(c)
            if expression_tree.rhs == None:
                expression_tree.operation = new_operation
                return expression_tree_builder(expression, expression_tree, i + 1)
            else:
                if expression_tree.operation < new_operation:
                    i, expression_tree.rhs = expression_tree_builder(
                        expression, AlgebraicExpression(), i - 1
                    )
                    return expression_tree_builder(expression, expression_tree, i + 1)
                else:
                    expression_tree.lhs = AlgebraicExpression(
                        expression_tree.lhs,
                        expression_tree.rhs,
                        expression_tree.operation,
                        expression_tree.function,
                    )
                    expression_tree.rhs = None
                    expression_tree.operation = new_operation
                    return expression_tree_builder(expression, expression_tree, i + 1)
    else:
        return i, expression_tree