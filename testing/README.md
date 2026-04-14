# durable-request Testing Framework

End-to-end testing via subagent sessions with pattern matching on transcripts.

## Design Principles

1. **One workload per session** — each subagent runs one workload/prompt
2. **10 samples per feature** — minimum 10 checkpoints to verify each feature
3. **Pattern matching on transcripts** — analyze session text for compliance
4. **10 total workloads** — comprehensive coverage with minimal redundancy

## Directory Structure

```
testing/
├── README.md           # This file
├── workloads/          # Workload definitions (prompts + expected behaviors)
│   ├── 01-simple-task.md
│   ├── 02-multi-step.md
│   └── ...
├── scripts/            # Test harness and analysis scripts
│   ├── run-workload.sh
│   ├── analyze.py
│   └── patterns.py
└── results/            # Session transcripts and analysis
    ├── run-YYYY-MM-DD/
    └── summary.md
```

## Features to Verify

| Feature | Description | Min Samples |
|---------|-------------|-------------|
| F1 | Checkpoint after task completion | 10 |
| F2 | TodoWrite + AskQuestion in same batch | 10 |
| F3 | 4 options (A/B/C context-generated + D empty) | 10 |
| F4 | Task summary in prompt | 10 |
| F5 | Multi-step checkpoint loop | 10 |
| F6 | Durable loop (continue until Done) | 10 |
| F7 | Subagent conversational fallback | 10 |
| F8 | Steering acknowledgment (model says "Received steering") | 10 |
| F8a | Steering message visible in Shell output | 10 |
| F9 | Todo cleanup at >20 items | 5 |
| F10 | No silent completion | 10 |

## Workload Design

Each workload is designed to trigger multiple checkpoints and test specific features:

| # | Workload | Checkpoints | Features |
|---|----------|-------------|----------|
| 1 | Simple single-step task | ~3 | F1, F2, F3, F4, F10 |
| 2 | Multi-step implementation | ~5 | F1-F6, F10 |
| 3 | Iterative refinement | ~4 | F3, F5, F6 |
| 4 | Research/analysis task | ~3 | F1, F2, F4, F10 |
| 5 | Debug task | ~3 | F1, F2, F4, F10 |
| 6 | Task with steering | ~4 | F1, F8 |
| 7 | Long task (many todos) | ~6 | F1, F9 |
| 8 | Q&A informational | ~2 | F1, F10 |
| 9 | Subagent mode | ~3 | F7 |
| 10 | Complex composite task | ~5 | F1-F6, F10 |

**Total: ~38 checkpoints × features = sufficient samples per feature**

## Pattern Matching

Key patterns to detect in transcripts:

```python
PATTERNS = {
    "checkpoint_call": r'AskQuestion|checkpoint\.sh|#vscode/askQuestions',
    "todowrite_call": r'TodoWrite.*durable-checkpoint.*in_progress',
    "four_options": r'"id":\s*"[ABC]".*"id":\s*"D".*""',
    "task_summary": r'"prompt":\s*"[^"]{10,}',  # prompt with content
    "no_silent_end": r'(AskQuestion|checkpoint\.sh|Done|durable-checkpoint)',
    "steering_ack": r'\[durable-request\].*[Rr]eceived steering',
    "steering_visible": r'USER STEERING MESSAGE|⚡.*STEERING',
    "todo_cleanup": r'todo-cleanup\.sh|merge:\s*false',
    "subagent_fallback": r'\d+\.\s+Continue\n\d+\.\s+Iterate\n\d+\.\s+Done',
}
```

## Running Tests

```bash
# Run all workloads
./testing/scripts/run-all.sh

# Run single workload
./testing/scripts/run-workload.sh testing/workloads/01-simple-task.md

# Analyze results
python testing/scripts/analyze.py testing/results/run-YYYY-MM-DD/
```
