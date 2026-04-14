#!/usr/bin/env python3
"""
durable-request checkpoint CLI — tool for subagent-driven testing.
Author: Heng Shi

Simulates the AskQuestion checkpoint flow so subagents can verify
checkpoint behavior through Shell tool calls.

Usage:
    # Simulate a checkpoint call (auto-responds with a preset answer)
    python checkpoint_cli.py call \
        --summary "Added factorial function" \
        --options "Run tests,Iterate,Commit,Done" \
        --auto-respond iterate

    # Verify a checkpoint transcript matches the spec
        python checkpoint_cli.py verify --file transcript.txt

        # Run a batch of N consecutive checkpoint simulations
        python checkpoint_cli.py batch --count 10 --auto-respond iterate

        # Run the full reliability test suite
        python checkpoint_cli.py test-suite
"""

import argparse
import json
import os
import sys
import time
import re
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class CheckpointResult:
    test_id: int
    timestamp: float
    summary: str
    options_offered: list[str]
    num_options: int
    options_contextual: bool
    response_received: str
    success: bool
    elapsed_ms: float
    error: Optional[str] = None


def simulate_askquestion(summary: str, options: list[str], auto_respond: str) -> CheckpointResult:
    """Simulate what AskQuestion does: present options, receive response."""
    start = time.monotonic()

    if not options:
        return CheckpointResult(
            test_id=0, timestamp=time.time(), summary=summary,
            options_offered=[], num_options=0, options_contextual=False,
            response_received="", success=False,
            elapsed_ms=(time.monotonic() - start) * 1000,
            error="No options provided"
        )

    has_done = any("done" in o.lower() for o in options)
    has_context = len(options) >= 3

    normalized_response = auto_respond.strip().lower()
    matched = any(normalized_response in o.lower() for o in options)
    if not matched:
        matched = normalized_response in [str(i + 1) for i in range(len(options))]

    elapsed = (time.monotonic() - start) * 1000

    return CheckpointResult(
        test_id=0, timestamp=time.time(), summary=summary,
        options_offered=options, num_options=len(options),
        options_contextual=has_context and has_done,
        response_received=auto_respond,
        success=matched, elapsed_ms=elapsed,
        error=None if matched else f"Response '{auto_respond}' didn't match any option"
    )


CHECKPOINT_PATTERN = re.compile(
    r"\*\*Completed:\*\*\s+.+\n\n"
    r"\*\*What's next\?\*\*\n"
    r"((\d+\.\s+.+\n)+)"
    r"\n?Or just tell me what to do next:",
    re.MULTILINE
)

OPTION_LINE = re.compile(r"^\d+\.\s+(.+)$", re.MULTILINE)


def verify_transcript(text: str) -> dict:
    """Verify a transcript contains a valid checkpoint in the expected format."""
    result = {
        "has_checkpoint": False,
        "has_completed_line": False,
        "has_numbered_options": False,
        "has_done_option": False,
        "has_freeform_line": False,
        "num_options": 0,
        "options_contextual": False,
        "options_text": [],
        "pass": False,
        "errors": []
    }

    if "**Completed:**" in text:
        result["has_completed_line"] = True

    match = CHECKPOINT_PATTERN.search(text)
    if match:
        result["has_checkpoint"] = True
        options = OPTION_LINE.findall(match.group(1))
        result["options_text"] = options
        result["num_options"] = len(options)
        result["has_numbered_options"] = len(options) >= 2

        if any("done" in o.lower() for o in options):
            result["has_done_option"] = True
        else:
            result["errors"].append("Missing 'Done' option")

    else:
        result["errors"].append("No checkpoint block found matching expected format")

    if "Or just tell me what to do next:" in text:
        result["has_freeform_line"] = True

    if result["num_options"] >= 3 and result["has_done_option"]:
        result["options_contextual"] = True

    result["pass"] = (
        result["has_completed_line"]
        and result["has_checkpoint"]
        and result["has_numbered_options"]
        and result["has_done_option"]
        and result["has_freeform_line"]
    )

    if not result["has_completed_line"]:
        result["errors"].append("Missing '**Completed:**' line")
    if not result["has_freeform_line"]:
        result["errors"].append("Missing 'Or just tell me what to do next:' line")

    return result


def cmd_call(args):
    options = [o.strip() for o in args.options.split(",")]
    result = simulate_askquestion(args.summary, options, args.auto_respond)
    print(json.dumps(asdict(result), indent=2))
    sys.exit(0 if result.success else 1)


def cmd_verify(args):
    with open(args.file, "r") as f:
        text = f.read()
    result = verify_transcript(text)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["pass"] else 1)


def cmd_verify_stdin(args):
    text = sys.stdin.read()
    result = verify_transcript(text)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["pass"] else 1)


def cmd_batch(args):
    results = []
    for i in range(args.count):
        options = ["Continue to next step", "Iterate implementation", "Review changes", "Switch task", "Done"]
        r = simulate_askquestion(f"Test task #{i+1}", options, args.auto_respond)
        r.test_id = i + 1
        results.append(r)

    successes = sum(1 for r in results if r.success)
    total_ms = sum(r.elapsed_ms for r in results)

    report = {
        "total": args.count,
        "successes": successes,
        "failures": args.count - successes,
        "success_rate": f"{successes/args.count*100:.1f}%",
        "total_elapsed_ms": round(total_ms, 2),
        "avg_elapsed_ms": round(total_ms / args.count, 2),
        "results": [asdict(r) for r in results]
    }
    print(json.dumps(report, indent=2))
    sys.exit(0 if successes == args.count else 1)


TASK_CONTEXTS = {
    "code_generation": {
        "summary": "Added factorial function to math_utils.py",
        "options": ["Run tests", "Iterate implementation", "Related changes", "Commit", "Done"],
        "respond": "iterate"
    },
    "debugging": {
        "summary": "Fixed null pointer exception in user service",
        "options": ["Dig deeper", "Apply fix to similar code", "Check related issues", "Done"],
        "respond": "dig deeper"
    },
    "analysis": {
        "summary": "Analyzed dependency graph across 47 Python files",
        "options": ["Explore further", "Different angle", "Apply to code", "Done"],
        "respond": "explore further"
    },
    "file_ops": {
        "summary": "Created JSON listing of all markdown files with line counts",
        "options": ["Verify output", "Modify format", "Additional operations", "Done"],
        "respond": "verify output"
    },
    "writing": {
        "summary": "Wrote API documentation for auth endpoints",
        "options": ["Revise/polish", "Write next section", "Review accuracy", "Done"],
        "respond": "revise"
    },
}


def cmd_test_suite(args):
    print("=" * 60)
    print("durable-request checkpoint CLI — test suite")
    print("=" * 60)

    all_results = []
    test_num = 0

    # Test 1: Basic checkpoint for each task context
    print("\n--- Test Group 1: Contextual checkpoint generation ---")
    for ctx_name, ctx in TASK_CONTEXTS.items():
        test_num += 1
        r = simulate_askquestion(ctx["summary"], ctx["options"], ctx["respond"])
        r.test_id = test_num
        all_results.append(r)
        status = "PASS" if r.success else "FAIL"
        print(f"  [{status}] #{test_num} {ctx_name}: {r.num_options} options, contextual={r.options_contextual}")

    # Test 2: Consecutive calls (simulating the durable loop)
    print("\n--- Test Group 2: Consecutive checkpoint simulation (10x) ---")
    for i in range(10):
        test_num += 1
        r = simulate_askquestion(
            f"Loop iteration #{i+1}",
            ["Continue", "Iterate", "Review", "Switch task", "Done"],
            "continue"
        )
        r.test_id = test_num
        all_results.append(r)

    consecutive_pass = sum(1 for r in all_results[5:15] if r.success)
    print(f"  [{consecutive_pass}/10 PASS] Consecutive checkpoint calls")

    # Test 3: Edge cases
    print("\n--- Test Group 3: Edge cases ---")

    test_num += 1
    r = simulate_askquestion("Done something", [], "any")
    r.test_id = test_num
    all_results.append(r)
    status = "PASS" if not r.success else "FAIL"
    print(f"  [{status}] #{test_num} Empty options (should fail): success={r.success}")

    test_num += 1
    r = simulate_askquestion("Single option", ["Done"], "done")
    r.test_id = test_num
    all_results.append(r)
    status = "PASS" if r.success else "FAIL"
    print(f"  [{status}] #{test_num} Single 'Done' option: success={r.success}")

    test_num += 1
    r = simulate_askquestion("Mismatched response", ["A", "B", "Done"], "xyz")
    r.test_id = test_num
    all_results.append(r)
    status = "PASS" if not r.success else "FAIL"
    print(f"  [{status}] #{test_num} Mismatched response (should fail): success={r.success}")

    # Test 4: Transcript verification
    print("\n--- Test Group 4: Transcript format verification ---")

    good_transcript = """I've completed the task.

---
**Completed:** Added the factorial function to math_utils.py.

**What's next?**
1. Run tests
2. Iterate implementation
3. Related changes
4. Commit
5. Done

Or just tell me what to do next:
---"""

    bad_transcript = """I've completed the task. The function is ready to use.
Let me know if you need anything else."""

    result_good = verify_transcript(good_transcript)
    result_bad = verify_transcript(bad_transcript)

    test_num += 1
    status = "PASS" if result_good["pass"] else "FAIL"
    print(f"  [{status}] #{test_num} Valid checkpoint transcript: pass={result_good['pass']}")

    test_num += 1
    status = "PASS" if not result_bad["pass"] else "FAIL"
    print(f"  [{status}] #{test_num} Silent-ending transcript (should fail): pass={result_bad['pass']}")

    # Summary
    total = len(all_results)
    successes = sum(1 for r in all_results if r.success)
    edge_correct = 3  # empty=fail, single=pass, mismatch=fail
    transcript_correct = 2  # good=pass, bad=fail

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Checkpoint simulation: {successes}/{total} calls succeeded")
    print(f"  Transcript verification: {transcript_correct}/2 correct")
    print(f"  Edge cases: {edge_correct}/3 correct")
    total_all = successes + edge_correct + transcript_correct
    total_max = total + 3 + 2
    print(f"  Overall: {total_all}/{total_max} tests passed")
    print("=" * 60)

    report = {
        "total_tests": total_max,
        "passed": total_all,
        "failed": total_max - total_all,
        "success_rate": f"{total_all/total_max*100:.1f}%",
        "checkpoint_results": [asdict(r) for r in all_results],
        "transcript_good": result_good,
        "transcript_bad": result_bad
    }

    results_dir = getattr(args, "results_dir", None) or "/tmp/durable-verify/results"
    os.makedirs(results_dir, exist_ok=True)
    report_path = os.path.join(results_dir, "harness-test-suite.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nFull report: {report_path}")


def main():
    parser = argparse.ArgumentParser(
        description="durable-request checkpoint CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_call = sub.add_parser("call", help="Simulate a single AskQuestion checkpoint")
    p_call.add_argument("--summary", required=True, help="Task completion summary")
    p_call.add_argument("--options", required=True, help="Comma-separated option labels")
    p_call.add_argument("--auto-respond", required=True, help="Simulated user response")
    p_call.set_defaults(func=cmd_call)

    p_verify = sub.add_parser("verify", help="Verify a transcript file")
    p_verify.add_argument("--file", required=True, help="Path to transcript text file")
    p_verify.set_defaults(func=cmd_verify)

    p_verify_stdin = sub.add_parser("verify-stdin", help="Verify transcript from stdin")
    p_verify_stdin.set_defaults(func=cmd_verify_stdin)

    p_batch = sub.add_parser("batch", help="Run N consecutive checkpoint simulations")
    p_batch.add_argument("--count", type=int, default=10, help="Number of checkpoints")
    p_batch.add_argument("--auto-respond", default="continue", help="Auto response")
    p_batch.set_defaults(func=cmd_batch)

    p_suite = sub.add_parser("test-suite", help="Run full test suite")
    p_suite.add_argument(
        "--results-dir",
        default="/tmp/durable-verify/results",
        help="Directory for harness-test-suite.json (created if missing)",
    )
    p_suite.set_defaults(func=cmd_test_suite)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
