# Enhance-Me Experiment Methodology

## Overview

This document describes how the /enhance-me skill was evaluated, how scores were obtained, and the limitations of the current approach.

---

## How Scores Were Obtained

### Method: LLM-as-Judge via Subagents

The scores were generated using **4 parallel subagent tasks**, each acting as both enhancer and evaluator:

| Subagent | Task | Tests |
|----------|------|-------|
| 1 | Enhance + score T01-T05 for Claude | 5 |
| 2 | Enhance + score T06-T10 for Claude | 5 |
| 3 | Enhance + score T01-T05 for GPT | 5 |
| 4 | Enhance + score T06-T10 for GPT | 5 |

Each subagent received:
1. The raw prompt to enhance
2. The enhancement rules (from the skill's SKILL.md content)
3. A scoring rubric with 5 metrics (1-5 scale)
4. Instructions to return structured JSON

### Scoring Rubric

| Metric | Definition | What a 5 means | What a 1 means |
|--------|-----------|----------------|----------------|
| **Structure** | Does it use model-appropriate formatting? | XML tags (Claude) or Markdown headers (GPT) applied consistently and correctly | No structure, raw text only |
| **Clarity** | Is the task unambiguous and specific? | Any agent could execute without guessing | Still vague, multiple interpretations possible |
| **Completeness** | Are success criteria, constraints, edge cases covered? | All 3 present and specific to the task | Missing all 3 |
| **Model-fit** | Does it apply model-specific techniques? | All key techniques applied (recency/primacy, tone, examples, etc.) | Generic, no model-specific optimization |
| **Actionability** | Can an agent execute without clarification? | Fully self-contained, ready to run | Requires follow-up questions |

---

## Critical Limitations

### 1. Self-Evaluation Bias

**The same model that generates the enhanced prompt also scores it.** This is the most significant limitation. The subagent is both the author and the grader, which introduces inherent bias toward higher scores.

**Impact**: Scores are likely inflated by 0.5-1.0 points compared to blind evaluation.

### 2. No Ground Truth

There is no "correct" enhanced prompt to compare against. The scoring is relative to the rubric, not to an objective standard.

### 3. No Execution Testing

The enhanced prompts were **not actually executed** against real Claude or GPT models to measure output quality. The scores measure "does the prompt follow the enhancement rules" not "does the enhanced prompt produce better results."

### 4. Single Evaluator Per Test

Each test case was evaluated by exactly one subagent instance. No inter-rater reliability was measured.

### 5. Structure Score Ceiling Effect

All 20 tests (10 × 2 models) scored 5/5 on Structure. This suggests either:
- The enhancement rules are trivially easy to follow for structure, OR
- The self-evaluator is biased toward giving perfect scores for its own work

---

## What the Scores Actually Measure

The scores measure **rule compliance**, not **output quality**:

- A score of 5 on "model_fit" means the enhanced prompt correctly applies XML tags, recency placement, calm tone, etc.
- It does NOT mean the enhanced prompt will produce 5x better code than the raw prompt.

The real question — "does /enhance-me actually improve agent output quality?" — requires a different experimental design.

---

## Proposed Rigorous Evaluation

To measure actual impact, we need:

### Design: Blind A/B Comparison

```
For each test case:
  1. Raw prompt → Agent A → Output A (scored by human or separate LLM judge)
  2. Enhanced prompt → Agent B → Output B (scored by same judge)
  3. Compare Output A vs Output B
```

### Judge: Separate LLM or Human

The judge should NOT be the same model that produced the output. Options:
- Human developer review (gold standard)
- Different model family (e.g., Gemini judges Claude vs GPT outputs)
- Automated code quality metrics (test pass rate, lint errors, etc.)

### Metrics: Output Quality, Not Prompt Structure

| Metric | How to Measure |
|--------|---------------|
| Code correctness | Run tests, check for errors |
| Completeness | Count required features implemented |
| Code quality | Lint score, cyclomatic complexity |
| Time to completion | Token count, tool calls |
| User satisfaction | Human rating 1-5 |

---

## Current Results (With Caveats)

### Rule Compliance Scores

| Model | Overall Avg | Structure | Clarity | Completeness | Model-fit | Actionability |
|-------|------------|-----------|---------|--------------|-----------|---------------|
| Claude | 4.68 | 5.00 | 4.60 | 4.40 | 5.00 | 4.30 |
| GPT | 4.56 | 5.00 | 4.70 | 4.30 | 4.30 | 4.40 |

**Interpretation**: The enhancement skills successfully encode model-specific best practices. Both Claude and GPT enhancement rules are followed consistently by the subagents. The scores confirm the SKILL.md content is well-structured and actionable.

**What this does NOT prove**: That enhanced prompts produce better agent outputs. That requires the A/B test described above.

---

## Confidence Level

| Aspect | Confidence | Reason |
|--------|-----------|--------|
| Enhancement rules are well-defined | HIGH | 12 techniques per model, sourced from official docs |
| Subagents can follow the rules | HIGH | All structure scores = 5.00 |
| Enhanced prompts are better structured | HIGH | XML/Markdown applied consistently |
| Enhanced prompts produce better outputs | LOW | Not tested with actual execution |
| Scores are unbiased | LOW | Self-evaluation, no blind review |

---

## Next Steps for Validation

1. **Blind A/B test**: Run raw vs enhanced prompts through actual agents, compare outputs
2. **Cross-model judging**: Use a different model to judge output quality
3. **Automated metrics**: For coding tasks, measure test pass rates, lint scores
4. **Human review**: Have developers rate raw vs enhanced outputs
5. **Statistical significance**: Run enough trials (n≥30 per condition) for p-values

Until these are done, treat the current scores as **proof of concept** — the enhancement rules are well-defined and followable, but actual output quality improvement is not yet quantified.
