#!/usr/bin/env python3
"""
Test runner for /enhance-me skill.

Uses subagents to enhance raw prompts and evaluates the results
against structured quality metrics. Generates statistical reports.

Usage:
    python testing/scripts/test-enhance.py [results-dir]

Results are saved to the specified directory (default: testing/results/enhance-run-YYYY-MM-DD/).
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Test cases: (id, raw_prompt, category)
TEST_CASES = [
    ("T01", "add auth to the app", "vague-coding"),
    ("T02", "I need a rate limiter for our API endpoints using Redis, make sure it handles edge cases and is tested", "specific-unstructured"),
    ("T03", "why is my react app slow", "debugging"),
    ("T04", "clean up the database module", "refactoring"),
    ("T05", "we need to add pagination to the user list page, currently it loads all users at once which is bad for performance, use the existing Pagination component in src/components/", "feature-with-context"),
    ("T06", "getting a 500 error on POST /api/checkout", "error-investigation"),
    ("T07", "write docs for the new API", "documentation"),
    ("T08", "review this PR and tell me what's wrong", "code-review"),
    ("T09", "should we use graphql or rest for the new service", "architecture-decision"),
    ("T10", "set up CI/CD for the project, we use GitHub Actions, need to build, test, and deploy to staging and production", "multi-step"),
]

METRICS = ["structure", "clarity", "completeness", "model_fit", "actionability"]
METRIC_LABELS = {
    "structure": "Structure (model-appropriate formatting)",
    "clarity": "Clarity (unambiguous, specific)",
    "completeness": "Completeness (success criteria, constraints, edge cases)",
    "model_fit": "Model-fit (recency/primacy, XML/Markdown, tone)",
    "actionability": "Actionability (executable without clarification)",
}


def load_test_cases():
    return TEST_CASES


def create_results_dir(base="testing/results"):
    timestamp = datetime.now().strftime("%Y-%m-%d")
    run_name = f"enhance-run-{timestamp}"
    results_dir = Path(base) / run_name
    results_dir.mkdir(parents=True, exist_ok=True)
    return results_dir


def save_results(results_dir, results):
    output_file = results_dir / "results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_file}")


def generate_report(results):
    """Generate a statistical summary report."""
    print("\n" + "=" * 70)
    print("ENHANCE-ME TEST RESULTS")
    print("=" * 70)

    all_scores = {"claude": {m: [] for m in METRICS}, "gpt": {m: [] for m in METRICS}}

    for test in results["tests"]:
        for model in ["claude", "gpt"]:
            scores = test[model]["scores"]
            for m in METRICS:
                all_scores[model][m].append(scores[m])

    for model in ["claude", "gpt"]:
        print(f"\n--- {model.upper()} ---")
        print(f"{'Metric':<45} {'Avg':>5} {'Min':>5} {'Max':>5} {'Std':>5}")
        print("-" * 70)
        for m in METRICS:
            vals = all_scores[model][m]
            avg = sum(vals) / len(vals)
            mn = min(vals)
            mx = max(vals)
            std = (sum((x - avg) ** 2 for x in vals) / len(vals)) ** 0.5
            print(f"{METRIC_LABELS[m]:<45} {avg:>5.2f} {mn:>5} {mx:>5} {std:>5.2f}")

        overall = [sum(all_scores[model][m][i] for m in METRICS) / len(METRICS)
                   for i in range(len(all_scores[model][METRICS[0]]))]
        avg_overall = sum(overall) / len(overall)
        print(f"\nOverall average: {avg_overall:.2f} / 5.00")

    # Per-test breakdown
    print(f"\n{'Test':<6} {'Category':<25} {'Claude':>8} {'GPT':>8} {'Delta':>8}")
    print("-" * 70)
    for test in results["tests"]:
        c_avg = sum(test["claude"]["scores"][m] for m in METRICS) / len(METRICS)
        g_avg = sum(test["gpt"]["scores"][m] for m in METRICS) / len(METRICS)
        delta = c_avg - g_avg
        print(f"{test['id']:<6} {test['category']:<25} {c_avg:>8.2f} {g_avg:>8.2f} {delta:>+8.2f}")

    print("\n" + "=" * 70)


def main():
    results_dir = create_results_dir()
    test_cases = load_test_cases()

    results = {
        "run_date": datetime.now().isoformat(),
        "skill_version": "1.0.0",
        "test_count": len(test_cases),
        "tests": [],
    }

    print(f"Enhance-me test runner — {len(test_cases)} test cases")
    print(f"Results directory: {results_dir}")
    print("\nThis script defines the test framework. To run actual tests,")
    print("use subagents to enhance each prompt and score the results.")
    print("\nTest cases defined:")
    for tid, prompt, cat in test_cases:
        print(f"  {tid} [{cat}]: {prompt[:60]}...")

    # Save the test case definitions
    save_results(results_dir, results)
    generate_report(results)

    return results_dir


if __name__ == "__main__":
    main()
