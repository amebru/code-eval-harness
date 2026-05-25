from __future__ import annotations
import sys
from typing import List, Dict
import re
from radon.complexity import cc_visit


def massage_test_list(code: str, test_list: List[str]) -> List[str]:
    """
    Replace the function name in the tests with the real one defined in the code.
    """
    if m := re.search(r"def\s+(\w+)\s*\(", code):
        func_name = m.group(1)
        return [
            (
                re.sub(r"assert (\w+)\(", f"assert {func_name}(", test.strip())
                if re.search(r"assert\s+\w+\s*\(", test)
                else test.strip()
            )
            for test in test_list
        ]
    else:
        return test_list


def evaluate_correctness(code: str, test_list: List[str]) -> float:
    results = []
    for s in test_list:
        # test_list is a list of assert statements to be evaluated in the context of `code`. run each assert
        # statement and record true/false whether it passed or failed
        try:
            exec(code + "\n" + s, {}, {})
            results.append(True)
        except AssertionError as ae:
            # print(
            #     f"Assertion failed for code `{code}` and test `{s}`: {s}\nError: {ae}",
            #     file=sys.stderr,
            # )
            results.append(False)
        except Exception as e:
            print(
                f"Error executing code `{code}` with test `{s}`: {s}\nError: {e}",
                file=sys.stderr,
            )
            results.append(False)

    return sum(results) / len(results) if results else 1.0


def evaluate_complexity(code: str) -> float:
    """
    1 is the least complex and 0 is the most complex
    """

    try:
        complexity = cc_visit(code)
        max_complexity = max(c.complexity for c in complexity) if complexity else 0
        return max(0.0, min(1.0, 1 - (max_complexity / 10)))
    except Exception as e:
        print(f"Error evaluating complexity for code `{code}`: {e}", file=sys.stderr)
        return 1.0  # be generous


def evaluate(code: str, test_list: List[str]) -> Dict[str, float]:
    correctness_score = evaluate_correctness(code, test_list)
    complexity_score = evaluate_complexity(code)
    return {
        "correctness": correctness_score,
        "complexity": complexity_score,
        "mean": (correctness_score + complexity_score) / 2,
    }


def evaluate_all(codes: List[str], test_lists: List[List[str]]) -> Dict[str, float]:
    test_lists = [
        massage_test_list(code, test_list) for code, test_list in zip(codes, test_lists)
    ]
    evaluations = [
        evaluate(code, test_list) for code, test_list in zip(codes, test_lists)
    ]
    mean_correctness = (
        sum(evaluation["correctness"] for evaluation in evaluations) / len(evaluations)
        if evaluations
        else 1.0
    )
    mean_complexity = (
        sum(evaluation["complexity"] for evaluation in evaluations) / len(evaluations)
        if evaluations
        else 1.0
    )
    return {
        "correctness": mean_correctness,
        "complexity": mean_complexity,
        "mean": (mean_correctness + mean_complexity) / 2,
    }
