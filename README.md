# Tasks

- evaluate.py
- expression.py -- Expression representation: AlgebraicExpression, Constant, Operation
- expression_builder.py -- string -> expression tree: using regular expression statemachines and recursion

## Expression representation

AlgebraicExpression(lhs, rhs, operation, function)

Example: sin(3*x) -> AlgebraicExpression(Constant(3), Variable(x), Operation("*"), Function("sin"))

## Expression building

1. expression_builder for integers without () and functions
2. expression_builder for floats without () and functions
3. expression_builder for floats with () but without functions
4. expression_builder for floats with () and functions
5. add variables