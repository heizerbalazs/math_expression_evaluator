# Math Expression Evaluator

Write a script that excepts two inputs:
- an arbitrary mathematical expression as a string
- value(s) to evaluate the expression at

and outputs the result or an error if the expression is invalid.

```
$ python evaluate.py --expression 'x*(x+1)' --at 4,5,6
>>
20.0, 30.0, 42.0

$ python evaluate.py --expression 'sin(x+1)x^2' --at 4
>>
-15.3278839446

```

# Requirements

- accept the following operators and functions:
    - +, -, *, /, ^ (power), % (mod)
    - sin, cos, tan, cot, exp, log

- handle arbitrary nested parentheses (round brackets)
- using ```eval``` or other available packages is not allowed, your code has to process the string and evaluate it directly.
