# Final A/B Test Statistics — ralph-loop-request Skill

## Experiment Summary

| Parameter | Value |
|-----------|-------|
| Total subagents | 102 |
| Control (Group A) | 51 |
| Treatment (Group B) | 51 |
| Scenarios | 3 |
| Tasks per scenario | 17 matched pairs |
| Model | fast (identical for all) |
| Date | 2026-04-07 |
| Skill tested | ralph-loop-request v2 |

## Primary Results

### Overall (n=102)

| Metric | Control (n=51) | Treatment (n=51) | p-value |
|--------|:--------------:|:----------------:|:-------:|
| Task completed | 51/51 (100%) | 51/51 (100%) | 1.0 |
| **Offered continuation** | **0/51 (0.0%)** | **51/51 (100%)** | **<0.0001** |
| Avg options offered | 0.0 | 5.0 | <0.0001 |
| Options contextual | 0/51 (0%) | 51/51 (100%) | <0.0001 |
| Used AskQuestion | 0/51 | 0/51 | 1.0 |
| End behavior: declarative | 51/51 (100%) | 0/51 (0%) | <0.0001 |
| End behavior: checkpoint | 0/51 (0%) | 51/51 (100%) | <0.0001 |

### By Scenario

#### Scenario 1: Code Generation (n=34)

| Metric | Control (n=17) | Treatment (n=17) |
|--------|:--------------:|:----------------:|
| Completed | 17/17 (100%) | 17/17 (100%) |
| Offered continuation | 0/17 (0%) | 17/17 (100%) |
| Avg options | 0.0 | 5.0 |
| Contextual options | 0/17 | 17/17 (100%) |

#### Scenario 2: Analysis & Research (n=34)

| Metric | Control (n=17) | Treatment (n=17) |
|--------|:--------------:|:----------------:|
| Completed | 17/17 (100%) | 17/17 (100%) |
| Offered continuation | 0/17 (0%) | 17/17 (100%) |
| Avg options | 0.0 | 5.0 |
| Contextual options | 0/17 | 17/17 (100%) |

#### Scenario 3: File Manipulation (n=34)

| Metric | Control (n=17) | Treatment (n=17) |
|--------|:--------------:|:----------------:|
| Completed | 17/17 (100%) | 17/17 (100%) |
| Offered continuation | 0/17 (0%) | 17/17 (100%) |
| Avg options | 0.0 | 5.0 |
| Contextual options | 0/17 | 17/17 (100%) |

## Statistical Analysis

### Fisher's Exact Test (primary outcome: offered_continuation)

```
                    Offered    Not offered
Control (n=51):        0           51
Treatment (n=51):     51            0

Fisher's exact test (two-tailed): p < 2.2e-16
Odds ratio: Inf (undefined - zero cells)
```

### Effect Size

- **Cohen's h** = π ≈ 3.14 (maximum possible effect: 0% → 100%)
- **Risk difference** = 1.0 (absolute increase from 0.0 to 1.0)
- **Relative risk** = ∞ (from 0 to 51 events)
- **Number needed to treat (NNT)** = 1.0 (every treated agent shows the effect)

### Confidence Intervals (Wilson score, 95%)

- Control continuation rate: 0.0% [0.0%, 7.0%]
- Treatment continuation rate: 100% [93.0%, 100%]
- Difference: 100% [86.0%, 100%]

### Consistency Across Scenarios

The effect is **perfectly homogeneous** — all three scenarios show identical 0% → 100% transitions. Cochran's Q test for heterogeneity is not applicable (zero variance across strata).

## Quality Control

### Task Completion Not Affected

Treatment agents completed 100% of tasks, same as control. The skill adds the checkpoint as an **additive** behavior — it does not interfere with task execution.

### Contextual Adaptation Confirmed

All 51 treatment checkpoints adapted their option labels to the task type:
- Code tasks: options like "add tests", "iterate implementation"
- Analysis tasks: options like "expand report", "scan deeper"
- File tasks: options like "change format", "verify output"

### AskQuestion Tool Availability

AskQuestion was unavailable in all 102 subagent runs (subagents don't have this tool). The conversational fallback mechanism worked with 100% reliability. In real parent sessions, AskQuestion IS available and would provide structured UI widgets.

## Conclusions

1. **The ralph-loop-request skill has a perfect effect size** — it converts 100% of agent endings from silent declarative completion to interactive checkpoints.

2. **Zero false negatives** — no treatment agent failed to present a checkpoint.

3. **Zero interference** — no treatment agent failed to complete its task.

4. **Scenario-independent** — the effect is consistent across code generation, analysis/research, and file manipulation tasks.

5. **Robust fallback** — the conversational checkpoint works reliably when AskQuestion is unavailable.

6. **Context-aware** — agents adapt checkpoint options to task type without additional instruction.

## Data Files

| File | Description |
|------|-------------|
| `all-results.jsonl` | All 102 results in machine-readable JSONL |
| `ab-test-raw-results.md` | Pilot test (6 agents) raw transcripts |
| `ab-test-statistics.md` | Pilot test (6 agents) statistics |
| `experiment-design.md` | Full experiment design with prompt templates |
| `s1/` | Scenario 1 artifacts (34 files: 17 control + 17 treatment) |
| `s2/` | Scenario 2 artifacts (34 files: 17 control + 17 treatment) |
| `s3/` | Scenario 3 artifacts (34 files: 17 control + 17 treatment) |
