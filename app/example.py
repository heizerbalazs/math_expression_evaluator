from operator import gt, lt, eq
from itertools import product

if __name__ == "__main__":
    case_sets = [
        (["+", "-"], ["+", "-"], [eq]),
        (["*", "/", "%"], ["*", "/", "%"], [eq]),
        (["^"], ["^"], [eq]),
    ]

    test_cases = [case for case_set in case_sets for case in product(*case_set)]
    print(test_cases)
