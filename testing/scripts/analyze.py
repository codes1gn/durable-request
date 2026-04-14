#!/usr/bin/env python3
"""
Analyze durable-request test session transcripts.

Usage:
    python analyze.py <results_dir>
    python analyze.py testing/results/run-2026-04-14/
"""

import sys
import json
import os
from pathlib import Path
from collections import defaultdict
from patterns import FEATURES, WORKLOAD_FEATURES, analyze_transcript, check_feature


def load_transcript(path: Path) -> str:
    """Load a transcript file (JSONL or text)."""
    content = path.read_text()
    
    if path.suffix == ".jsonl":
        # Extract text content from JSONL
        lines = []
        for line in content.strip().split("\n"):
            try:
                obj = json.loads(line)
                if "content" in obj:
                    lines.append(obj["content"])
                elif "message" in obj:
                    lines.append(obj["message"])
            except json.JSONDecodeError:
                lines.append(line)
        return "\n".join(lines)
    else:
        return content


def analyze_results_dir(results_dir: Path) -> dict:
    """Analyze all transcripts in a results directory."""
    feature_samples = defaultdict(list)
    workload_results = []
    
    for transcript_file in sorted(results_dir.glob("*.jsonl")) + sorted(results_dir.glob("*.txt")):
        # Extract workload ID from filename (e.g., "01-simple-task-001.jsonl")
        name = transcript_file.stem
        parts = name.rsplit("-", 1)
        if len(parts) == 2 and parts[1].isdigit():
            workload_id = parts[0]
        else:
            workload_id = name
        
        transcript = load_transcript(transcript_file)
        result = analyze_transcript(transcript, workload_id)
        result["file"] = transcript_file.name
        workload_results.append(result)
        
        # Collect samples per feature
        for fid, data in result["features"].items():
            feature_samples[fid].append({
                "file": transcript_file.name,
                "found": data["found"],
                "count": data.get("count", 0)
            })
    
    # Compute feature statistics
    feature_stats = {}
    for fid, samples in feature_samples.items():
        passed = sum(1 for s in samples if s["found"])
        total = len(samples)
        min_required = FEATURES[fid].min_samples
        
        feature_stats[fid] = {
            "name": FEATURES[fid].name,
            "passed": passed,
            "total": total,
            "success_rate": passed / total if total > 0 else 0,
            "min_required": min_required,
            "sufficient_samples": total >= min_required,
            "meets_criteria": passed >= min_required
        }
    
    return {
        "workloads": workload_results,
        "features": feature_stats,
        "summary": {
            "total_sessions": len(workload_results),
            "features_tested": len(feature_stats),
            "features_passed": sum(1 for f in feature_stats.values() if f["meets_criteria"])
        }
    }


def print_report(analysis: dict):
    """Print a formatted analysis report."""
    print("=" * 60)
    print("DURABLE-REQUEST TEST ANALYSIS REPORT")
    print("=" * 60)
    print()
    
    summary = analysis["summary"]
    print(f"Total sessions analyzed: {summary['total_sessions']}")
    print(f"Features tested: {summary['features_tested']}")
    print(f"Features passing: {summary['features_passed']}/{summary['features_tested']}")
    print()
    
    print("-" * 60)
    print("FEATURE RESULTS")
    print("-" * 60)
    print(f"{'Feature':<6} {'Name':<40} {'Pass Rate':<12} {'Status'}")
    print("-" * 60)
    
    for fid in sorted(analysis["features"].keys()):
        data = analysis["features"][fid]
        rate = f"{data['passed']}/{data['total']}"
        pct = f"({data['success_rate']:.0%})"
        
        if data["meets_criteria"]:
            status = "✓ PASS"
        elif not data["sufficient_samples"]:
            status = "⚠ NEED MORE SAMPLES"
        else:
            status = "✗ FAIL"
        
        name = data["name"][:38] + ".." if len(data["name"]) > 40 else data["name"]
        print(f"{fid:<6} {name:<40} {rate:<6} {pct:<5} {status}")
    
    print()
    print("-" * 60)
    print("WORKLOAD RESULTS")
    print("-" * 60)
    
    for result in analysis["workloads"]:
        status = "✓" if result["passed"] == result["total"] else "✗"
        print(f"{status} {result['file']}: {result['passed']}/{result['total']} features")
    
    print()
    print("=" * 60)
    
    # Final verdict
    if summary["features_passed"] == summary["features_tested"]:
        print("OVERALL: ✓ ALL FEATURES PASS")
    else:
        failed = summary["features_tested"] - summary["features_passed"]
        print(f"OVERALL: ✗ {failed} FEATURE(S) NEED ATTENTION")


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze.py <results_dir>")
        sys.exit(1)
    
    results_dir = Path(sys.argv[1])
    if not results_dir.exists():
        print(f"Error: Directory not found: {results_dir}")
        sys.exit(1)
    
    analysis = analyze_results_dir(results_dir)
    print_report(analysis)
    
    # Save JSON report
    report_file = results_dir / "analysis.json"
    with open(report_file, "w") as f:
        json.dump(analysis, f, indent=2, default=str)
    print(f"\nDetailed report saved to: {report_file}")


if __name__ == "__main__":
    main()
