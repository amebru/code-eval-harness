from __future__ import annotations
from typing import Dict, List


def report(model_scores: Dict[str, Dict[str, float]]) -> None:
    print("Evaluation Report:")
    # print model_scores as a table
    print(f"{'Model':<20} {'Correctness':<15} {'Complexity':<15} {'Mean':<15}")
    print("-" * 57)
    for model_name, scores in model_scores.items():
        print(
            f"{model_name:<20} {scores['correctness']:<15.2f} {scores['complexity']:<15.2f} {scores['mean']:<15.2f}"
        )
