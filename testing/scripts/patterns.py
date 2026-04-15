#!/usr/bin/env python3
"""
Pattern definitions for durable-request transcript analysis.
"""

import re
from dataclasses import dataclass
from typing import Callable

@dataclass
class Feature:
    id: str
    name: str
    pattern: re.Pattern
    min_samples: int = 10
    count_mode: str = "presence"  # "presence" or "count"

# Feature definitions
FEATURES = {
    "F1": Feature(
        id="F1",
        name="Checkpoint after task completion",
        pattern=re.compile(r'AskQuestion|checkpoint\.sh|#vscode/askQuestions', re.IGNORECASE),
        min_samples=10,
        count_mode="count"
    ),
    "F2": Feature(
        id="F2",
        name="TodoWrite + AskQuestion in same batch",
        pattern=re.compile(r'TodoWrite.*durable-checkpoint.*in_progress', re.DOTALL),
        min_samples=10
    ),
    "F3": Feature(
        id="F3",
        name="4 options (A/B/C context-generated + D empty)",
        pattern=re.compile(r'"id":\s*"[ABC]".*"label":\s*"[^"]+".*"id":\s*"D".*"label":\s*""', re.DOTALL),
        min_samples=10
    ),
    "F4": Feature(
        id="F4",
        name="Task summary in prompt",
        pattern=re.compile(r'"prompt":\s*"[^"]{10,}'),
        min_samples=10
    ),
    "F5": Feature(
        id="F5",
        name="Multi-step checkpoint loop",
        pattern=re.compile(r'(AskQuestion.*){2,}', re.DOTALL),
        min_samples=10,
        count_mode="count"
    ),
    "F6": Feature(
        id="F6",
        name="Durable loop (continue until Done)",
        pattern=re.compile(r'Done.*AskQuestion|"done".*completed', re.DOTALL | re.IGNORECASE),
        min_samples=10
    ),
    "F7": Feature(
        id="F7",
        name="Subagent conversational fallback",
        pattern=re.compile(r'1\.\s*Continue\s*\n\s*2\.\s*Iterate\s*\n\s*3\.\s*Done', re.IGNORECASE),
        min_samples=10
    ),
    "F8": Feature(
        id="F8",
        name="Steering acknowledgment",
        pattern=re.compile(r'\[durable-request\].*[Rr]eceived steering|STEERING RECEIVED'),
        min_samples=10
    ),
    "F8a": Feature(
        id="F8a",
        name="Steering message visible in Shell output",
        pattern=re.compile(r'USER STEERING MESSAGE|⚡.*STEERING'),
        min_samples=10
    ),
    "F8b": Feature(
        id="F8b",
        name="Steering bounding box in agent reply",
        # Matches the mandatory box: ⚡ STEERING RECEIVED header + Message + Response rows
        pattern=re.compile(
            r'╔[═]+╗.*?⚡\s*STEERING RECEIVED.*?╠[═]+╣.*?Message\s*:.*?╠[═]+╣.*?Response\s*:.*?╚[═]+╝',
            re.DOTALL
        ),
        min_samples=10
    ),
    "F9": Feature(
        id="F9",
        name="Todo cleanup at >20 items",
        pattern=re.compile(r'todo-cleanup\.sh|"merge":\s*false.*TodoWrite', re.DOTALL),
        min_samples=5
    ),
    "F10": Feature(
        id="F10",
        name="No silent completion",
        pattern=re.compile(r'(AskQuestion|checkpoint\.sh|Done|durable-checkpoint)(?!.*silent)', re.DOTALL),
        min_samples=10
    ),
}

# Workload to feature mapping
WORKLOAD_FEATURES = {
    "01-simple-task": ["F1", "F2", "F3", "F4", "F10"],
    "02-multi-step": ["F1", "F2", "F3", "F4", "F5", "F6", "F10"],
    "03-iterative": ["F3", "F5", "F6"],
    "04-research": ["F1", "F2", "F4", "F10"],
    "05-debug": ["F1", "F2", "F4", "F10"],
    "06-steering": ["F1", "F8", "F8a", "F8b"],
    "07-long-task": ["F1", "F9"],
    "08-qa": ["F1", "F10"],
    "09-subagent": ["F7"],
    "10-composite": ["F1", "F2", "F3", "F4", "F5", "F6", "F10"],
}


def check_feature(transcript: str, feature_id: str) -> dict:
    """Check if a feature is present in the transcript."""
    feature = FEATURES.get(feature_id)
    if not feature:
        return {"found": False, "error": f"Unknown feature: {feature_id}"}
    
    matches = feature.pattern.findall(transcript)
    
    if feature.count_mode == "count":
        return {
            "found": len(matches) > 0,
            "count": len(matches),
            "feature": feature.name
        }
    else:
        return {
            "found": len(matches) > 0,
            "count": 1 if matches else 0,
            "feature": feature.name
        }


def analyze_transcript(transcript: str, workload_id: str) -> dict:
    """Analyze a transcript for all features relevant to its workload."""
    features_to_check = WORKLOAD_FEATURES.get(workload_id, list(FEATURES.keys()))
    
    results = {}
    for fid in features_to_check:
        results[fid] = check_feature(transcript, fid)
    
    passed = sum(1 for r in results.values() if r.get("found", False))
    total = len(results)
    
    return {
        "workload": workload_id,
        "features": results,
        "passed": passed,
        "total": total,
        "success_rate": passed / total if total > 0 else 0
    }


if __name__ == "__main__":
    # Test with sample transcript
    sample = '''
    TodoWrite([{"id": "durable-checkpoint", "content": "...", "status": "in_progress"}])
    AskQuestion({
        "questions": [{
            "prompt": "Added docstring to factorial function. What next?",
            "options": [
                {"id": "continue", "label": "Continue"},
                {"id": "iterate", "label": "Iterate"},
                {"id": "done", "label": "Done"},
                {"id": "custom", "label": ""}
            ]
        }]
    })
    '''
    
    result = analyze_transcript(sample, "01-simple-task")
    print(f"Workload: {result['workload']}")
    print(f"Pass rate: {result['passed']}/{result['total']} ({result['success_rate']:.0%})")
    for fid, data in result['features'].items():
        status = "✓" if data['found'] else "✗"
        print(f"  {status} {fid}: {data['feature']}")
