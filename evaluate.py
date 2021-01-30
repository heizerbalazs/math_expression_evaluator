#! /Users/balazsheizer/DEV/homework/.env/bin/python
import argparse
from typing import List

from app.expression_builder import ExpressionTreeBuilder


def evaluate(expression: str, at: List[float]) -> int:
    _, expr = ExpressionTreeBuilder(expression, {"x": 0}).build_expression()
    at = [{"x": v} for v in at]
    return list(map(lambda x: expr.evaluate(x), at))


def parse_args():
    parser = argparse.ArgumentParser(__name__)
    parser.add_argument(
        "--expression", type=str, help="the expression you want to evaluate"
    )
    parser.add_argument(
        "--at",
        type=lambda s: [int(item) for item in s.split(",")],
        help="point\\points where you want to know the value of the expression",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    expression = args.expression
    at = args.at
    values = evaluate(expression, at)
    print(">>")
    print(*values, sep=", ")
