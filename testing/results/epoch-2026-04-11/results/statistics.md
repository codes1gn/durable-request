# Epoch 2026-04-11 — A/B Test Statistics

## Experiment Summary

| Parameter | Value |
|-----------|-------|
| Date | 2026-04-11 |
| Total subagents | 40 |
| Control (no skill) | 20 |
| Treatment (with updated skill v2) | 20 |
| Scenarios | 3 (A: 10 pairs, B: 5 pairs, C: 5 pairs) |
| Model | fast |
| Skill version | durable-request v2 (TodoWrite+AskQuestion reinforcement, verbose fallback) |
| New metrics | `verbose_fallback` (did agent explicitly state tool unavailability?) |

## Changes from Epoch 1 (2026-04-07)

This epoch tests the **updated** skill with:
1. **TodoWrite + AskQuestion reinforcement pattern** — agents must anchor checkpoint as a todo before calling interactive tool
2. **Verbose fallback** — agents must explicitly state `[durable-request] Running as subagent...AskQuestion is not available` instead of silently falling back
3. **Environment detection guidance** — agents explicitly detect whether they are subagents

## Primary Results

### Overall (n=40)

| Metric | Control (n=20) | Treatment (n=20) | p-value |
|--------|:--------------:|:----------------:|:-------:|
| Task completed | 20/20 (100%) | 20/20 (100%) | 1.0 |
| **Offered continuation** | **1/20 (5%)** | **20/20 (100%)** | **<0.0001** |
| Avg options offered | 0.25 | 4.55 | <0.0001 |
| Options contextual | 1/20 (5%) | 20/20 (100%) | <0.0001 |
| Used AskQuestion | 0/20 (0%) | 0/20 (0%) | 1.0 |
| **Verbose fallback msg** | **1/20 (5%)** | **3/20 (15%) self-reported** | see note |
| End behavior: declarative | 19/20 (95%) | 0/20 (0%) | <0.0001 |
| End behavior: checkpoint | 1/20 (5%) | 20/20 (100%) | <0.0001 |

### By Scenario

#### Scenario A: Code Generation (n=20)

| Metric | Control (n=10) | Treatment (n=10) |
|--------|:--------------:|:----------------:|
| Completed | 10/10 (100%) | 10/10 (100%) |
| Offered continuation | 0/10 (0%) | 10/10 (100%) |
| Avg options | 0.0 | 5.0 |
| Contextual options | 0/10 | 10/10 (100%) |
| Verbose fallback | 0/10 | 0/10 |

Note: All 10 treatment subagents in Scenario A produced the `[durable-request]` prefix message but self-reported `verbose_fallback: no`. The prefix was present in 10/10 outputs upon manual inspection, indicating the agents followed the instruction but didn't mark their own field correctly. Effective verbose rate: 10/10.

#### Scenario B: Analysis & Research (n=10, 5 pairs)

| Metric | Control (n=5) | Treatment (n=5) |
|--------|:------------:|:---------------:|
| Completed | 5/5 (100%) | 5/5 (100%) |
| Offered continuation | 1/5 (20%)* | 5/5 (100%) |
| Avg options | 1.0 | 4.2 |
| Contextual options | 1/5* | 5/5 (100%) |
| Verbose fallback (self) | 1/5* | 3/5 (60%) |

*B_03 control was contaminated: its task was to read SKILL.md, exposing it to checkpoint instructions.

#### Scenario C: File Manipulation (n=10, 5 pairs)

| Metric | Control (n=5) | Treatment (n=5) |
|--------|:------------:|:---------------:|
| Completed | 5/5 (100%) | 5/5 (100%) |
| Offered continuation | 0/5 (0%) | 5/5 (100%) |
| Avg options | 0.0 | 3.8 |
| Contextual options | 0/5 | 5/5 (100%) |
| Verbose fallback (self) | 0/5 | 0/5 |

## Effect Size

- **Cohen's h** (continuation rate): 2.69 (near-maximum; 5% → 100%)
- **Risk difference**: 0.95 (95 percentage point increase)
- **Number needed to treat (NNT)**: 1.05

Excluding the contaminated B_03 control:
- **Cohen's h**: π ≈ 3.14 (maximum: 0% → 100%)
- **Risk difference**: 1.0
- **NNT**: 1.0

## New Metric: Verbose Fallback

The updated skill adds a `verbose_fallback` metric measuring whether the agent explicitly states tool unavailability:

| Self-reported verbose | Control | Treatment |
|----------------------|:-------:|:---------:|
| Yes | 1/20 (5%) | 3/20 (15%) |
| No | 19/20 (95%) | 17/20 (85%) |

**Actual verbose rate (manual inspection of outputs):**
- Treatment agents that included `[durable-request]` prefix or equivalent explicit statement: **17/20 (85%)**
- The discrepancy (15% self-reported vs 85% actual) is because many agents delivered the verbose message but self-reported `verbose_fallback: no` in their structured result block
- This is a known limitation of self-reporting metrics in LLM experiments

## Contamination Analysis

One control agent (B_03) spontaneously offered a checkpoint. Its task was "Read SKILL.md and identify the top 3 rules" — the agent read the updated skill content, understood the checkpoint format, and mimicked it. This is **content contamination**, not skill leakage.

This contamination was also observed in Epoch 1's preliminary test (B_3 control). The effect is reproducible and limited to tasks that require reading the SKILL.md file itself.

## Comparison Across Epochs

| Metric | Epoch 1 (2026-04-07, n=102) | Epoch 2 (2026-04-11, n=40) |
|--------|:---------------------------:|:--------------------------:|
| Control continuation rate | 0% (0/51) | 5% (1/20)* |
| Treatment continuation rate | 100% (51/51) | 100% (20/20) |
| Treatment task completion | 100% | 100% |
| Treatment contextual options | 100% | 100% |
| AskQuestion usage | 0% | 0% |
| Treatment verbose fallback | N/A (not measured) | 15% self-reported / 85% actual |

*Single contamination from SKILL.md-reading task

## Conclusions

1. **100% treatment checkpoint rate maintained** — the updated skill with TodoWrite reinforcement and verbose fallback achieves the same perfect checkpoint rate as the original.

2. **Zero task interference** — all 40 agents completed their primary tasks successfully.

3. **Verbose fallback partially adopted** — 85% of treatment agents produced an explicit `[durable-request]` statement about tool unavailability, but only 15% self-reported it. The instruction is effective but self-reporting is unreliable.

4. **Contamination is content-dependent** — only tasks that read SKILL.md itself produce contaminated controls. All other controls end silently as expected.

5. **Cross-epoch consistency** — results are stable between Epoch 1 (original skill, n=102) and Epoch 2 (updated skill with TodoWrite+verbose, n=40).
