def check_parentheses(expression: str) -> bool:
    p_open = 0
    p_close = 0
    for i, c in enumerate(expression):
        p_open += 1 if c == "(" else 0
        p_close += 1 if c == ")" else 0

        if p_open < p_close:
            return False

    return True if p_open == p_close else False


def check_type(expression: str) -> str:
    operators = ["+", "-", "*", "/", "%", "^"]
    functions = ["sin", "cos", "tan", "log", "exp"]

    # if all open parenthesis are closed then this part is the lhs
    # if ther is no parenthesis then the expression before the first operator is the lhs
    # if there is an operator after lhs the remaining part is the rhs
    # if the lhs starts with function name then it is a function expression
    # else it can be an expression, a  variable or a constant

    if expression == "x":
        return "variable"
    elif any([o in expression for o in operators]):
        return "expression"
    elif (expression[3] == "(") and (expression[-1] == ")"):
        return "function"
    else:
        return "constant"