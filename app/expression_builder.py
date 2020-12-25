from app.expression import AlgebraicExpression, Operation, Constant


def is_digit(c):
    digits = list(map(lambda x: str(x), [i for i in range(10)]))
    return c in digits


def is_operaton(c):
    operations = Operation.prioroties.keys()
    return c in operations


def expression_tree_builder(
    expression: str, i: int = 0, operation: Operation = Operation("+")
) -> AlgebraicExpression:
    n = len(expression)
    expression_tree = AlgebraicExpression()
    while i < n:
        c = expression[i]
        if is_digit(c) & (expression_tree.lhs != None):
            expression_tree.rhs = Constant(float(c))
        if is_digit(c) & (expression_tree.lhs == None):
            expression_tree.lhs = Constant(float(c))
        if is_operaton(c):
            new_operation = Operation(c)
            if expression_tree.rhs == None:
                expression_tree.operation = new_operation
            else:
                if expression_tree.operation <= new_operation:
                    i, expression_tree.rhs = expression_tree_builder(expression, i - 1)
                else:
                    expression_tree.lhs = AlgebraicExpression(
                        expression_tree.lhs,
                        expression_tree.rhs,
                        expression_tree.operation,
                        expression_tree.function,
                    )
                    expression_tree.rhs = None
                    expression_tree.operation = new_operation

        i += 1

    return i, expression_tree
