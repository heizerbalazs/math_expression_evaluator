# Tasks

- evaluate.py
- expression.py -- Expression representation: AlgebraicExpression, Constant, Operation
- expression_builder.py -- string -> expression tree: using regular expression statemachines

# Expression representation

AlgebraicExpression(lhs, rhs, operation, function)

Example: sin(3*x) -> AlgebraicExpression(Constant(3), Variable(x), Operation("*"), Function("sin"))

# Expression building
