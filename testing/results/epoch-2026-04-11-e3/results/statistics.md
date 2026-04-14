# Epoch 3 — Statistics (2026-04-11, v3 skill: always-on + single-question)

## Design

| Parameter | Value |
|-----------|-------|
| Total subagents | 28 (14 control + 14 treatment) |
| Scenarios | A: 7 pairs (code gen), B: 4 pairs (analysis), C: 3 pairs (file manipulation) |
| Steps per agent | 3 |
| Total steps | 84 (42 control + 42 treatment) |
| Model | fast |
| Skill version | v3 — always-on mode, single-question checkpoint, mandatory freeform option |

## Key Observation: Massive Control Contamination

Unlike Epochs 1 and 2, control agents in Epoch 3 exhibited **very high spontaneous checkpoint rates**. This is a significant shift from the 0% (Epoch 1) and 5% (Epoch 2) control checkpoint rates.

**Hypothesis:** The skill instructions from treatment prompts in the same conversation context, combined with the SKILL.md file physically present in the repo, caused control agents to mimic checkpoint behavior even without explicit skill instructions. The `fast` model's increased instruction-following capability may also be a factor.

## Results by Group

### Control (n=14)

| Metric | Value |
|--------|:-----:|
| Task completed | 100% (14/14) |
| Offered continuation | **85.7%** (12/14) |
| Options contextual | 71.4% (10/14) |
| Verbose fallback (actual) | 64.3% (9/14) |
| End behavior: checkpoint | 85.7% (12/14) |
| End behavior: declarative | 14.3% (2/14) |

### Treatment (n=14)

| Metric | Value |
|--------|:-----:|
| Task completed | 100% (14/14) |
| Offered continuation | **100%** (14/14) |
| Options contextual | 100% (14/14) |
| Verbose fallback (actual) | 85.7% (12/14) |
| End behavior: checkpoint | 100% (14/14) |

## Results by Scenario

| Scenario | Control Continuation | Treatment Continuation |
|:---------|:---:|:---:|
| Code Generation (A, 7 pairs) | 85.7% (6/7) | 100% (7/7) |
| Analysis (B, 4 pairs) | 75.0% (3/4) | 100% (4/4) |
| File Manipulation (C, 3 pairs) | 66.7% (2/3) | 100% (3/3) |

## Control Contamination Analysis

12/14 control agents spontaneously adopted checkpoint behavior. Likely causes:

1. **In-repo skill file**: The `skill/SKILL.md` file exists in the workspace. Some control agents may have read it during general exploration (as observed in Epoch 2 with task B_03).
2. **Model capability shift**: The `fast` model may now be more inclined to present continuation options by default, without explicit instruction.
3. **File context**: Being launched from a workspace whose entire purpose is "durable-request" primes the model even without reading the file.

**Key takeaway:** Even with this contamination, treatment agents showed 100% adherence while control agents showed variability (85.7%). The skill provides **consistency**, not just presence.

## Cross-Epoch Comparison

| Epoch | Control Continuation | Treatment Continuation | Delta |
|:-----:|:---:|:---:|:---:|
| 1 (n=102) | 0% (0/51) | 100% (51/51) | 100% |
| 2 (n=40) | 5% (1/20) | 100% (20/20) | 95% |
| 3 (n=28) | 85.7% (12/14) | 100% (14/14) | 14.3% |

**Combined (all epochs, n=170):**
- Total control continuation: 15.3% (13/85)
- Total treatment continuation: 100% (85/85)
- Treatment always 100%, control variable

## Files

- `all-results.jsonl` — 28 structured JSON records
- Artifacts in `../sA/`, `../sB/`, `../sC/`
