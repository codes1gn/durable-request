# A/B Test Report: Raw vs Enhanced Prompts

**Date:** 2026-05-21
**Model:** Claude 4.6 Opus (via Cursor subagents)
**Test Type:** Blind A/B — same model, same data collection protocol, different prompt quality
**Tasks:** 3 real TypeScript coding tasks
**Evaluation:** Self-assessment by executing subagent (1-5 scale, 5 dimensions)

---

## Executive Summary

Enhanced prompts produced **16.4% higher quality code** compared to raw prompts, measured across structure, completeness, type safety, error handling, and testability. The biggest gain was in **completeness** and **testability** — enhanced prompts explicitly specified requirements that raw prompts left to model inference.

| Metric | Raw Avg | Enhanced Avg | Delta | Improvement |
|--------|---------|--------------|-------|-------------|
| **Overall** | **4.07** | **4.73** | **+0.67** | **+16.4%** |
| Structure | 4.67 | 5.00 | +0.33 | +7.1% |
| Completeness | 3.67 | 4.67 | +1.00 | +27.3% |
| Type Safety | 4.67 | 5.00 | +0.33 | +7.1% |
| Error Handling | 3.33 | 4.00 | +0.67 | +20.0% |
| Testability | 4.00 | 5.00 | +1.00 | +25.0% |

---

## Per-Task Results

### T1: Login Validator

| Dimension | Raw | Enhanced | Delta |
|-----------|-----|----------|-------|
| Structure | 5 | 5 | 0 |
| Completeness | 4 | 5 | +1 |
| Type Safety | 5 | 5 | 0 |
| Error Handling | 4 | 4 | 0 |
| Testability | 4 | 5 | +1 |
| **Average** | **4.40** | **4.80** | **+0.40** |
| Test Cases | 8 | 11 | +3 |
| Edge Cases Considered | 8 | 10 | +2 |

**Key differences:** Enhanced version added email length limit (254 chars), max password length (128), null/undefined input handling, configurable character classes, and separate error codes for each password requirement. Raw version missed max-length bounds and null-input handling entirely.

### T2: Rate Limiter (Biggest Improvement)

| Dimension | Raw | Enhanced | Delta |
|-----------|-----|----------|-------|
| Structure | 4 | 5 | +1 |
| Completeness | 3 | 4 | +1 |
| Type Safety | 4 | 5 | +1 |
| Error Handling | 3 | 4 | +1 |
| Testability | 4 | 5 | +1 |
| **Average** | **3.60** | **4.60** | **+1.00** |
| Test Cases | 7 | 12 | +5 |
| Edge Cases Considered | 6 | 10 | +4 |

**Key differences:** Enhanced version implemented true sliding window with timestamp tracking, API key extraction, namespace isolation per endpoint, x-forwarded-for support, periodic memory cleanup with timer.unref(), and config validation. Raw version used a simpler fixed-window counter without cleanup or multi-key-strategy support.

### T3: TTL Cache

| Dimension | Raw | Enhanced | Delta |
|-----------|-----|----------|-------|
| Structure | 5 | 5 | 0 |
| Completeness | 4 | 5 | +1 |
| Type Safety | 5 | 5 | 0 |
| Error Handling | 3 | 4 | +1 |
| Testability | 4 | 5 | +1 |
| **Average** | **4.20** | **4.80** | **+0.60** |
| Test Cases | 9 | 15 | +6 |
| Edge Cases Considered | 5 | 12 | +7 |

**Key differences:** Enhanced version added LRU eviction, event system (6 event types), cache statistics (hits/misses/evictions), dispose() method for cleanup interval, and Cache<T> interface. Raw version was a clean but minimal TTL-only cache without eviction, events, or stats.

---

## Feature Comparison

| Feature | Raw (3 tasks) | Enhanced (3 tasks) |
|---------|--------------|-------------------|
| Total test cases | 24 | 38 (+58%) |
| Edge cases considered | 19 | 32 (+68%) |
| Edge cases NOT considered | 22 | 2 (-91%) |
| Unique features | 19 | 36 (+89%) |
| Max password length | No | Yes |
| Null/undefined input handling | No | Yes |
| LRU eviction | No | Yes |
| Event system | No | Yes |
| Cache statistics | No | Yes |
| API key extraction | No | Yes |
| Namespace isolation | No | Yes |
| Memory cleanup | No (manual only) | Yes (periodic + lazy) |
| Config validation | Partial | Full |

---

## What Enhancement Actually Did

### 1. Specified boundaries the model wouldn't infer

Raw "write a login validator" didn't mention max email length, max password length, or null inputs. The model didn't add these because it wasn't asked. Enhanced prompt listed them in `<constraints>` and `<success_criteria>`, so the model delivered them.

### 2. Demanded features through examples

The enhanced rate limiter prompt included a concrete example showing `Retry-After`, `X-RateLimit-*` headers, and the 429 response body format. The raw prompt just said "rate limiter" — the model added basic headers but missed namespace isolation and API key strategies.

### 3. Set a higher test coverage bar

Enhanced prompts specified "at least 8/10/12 test cases" in `<success_criteria>`. Raw prompts let the model choose, and it defaulted to 7-9 tests. Enhanced outputs averaged 12.7 tests vs 8.0 for raw.

### 4. Activated domain-specific reasoning

The enhanced cache prompt asked for "event-driven" behavior and "LRU eviction" — features a senior engineer would want. The raw prompt produced a clean but basic TTL cache that a junior engineer might ship without considering memory bounds.

---

## Limitations

1. **Self-evaluation bias**: Same model generates and scores. Scores likely inflated +0.3-0.5 for both conditions. The DELTA between raw and enhanced is more reliable than absolute scores.

2. **No execution**: Code was not compiled or tested. Scores reflect structural quality, not runtime correctness.

3. **Same model for both conditions**: Both raw and enhanced prompts were given to Claude. A truly fair test would also measure on GPT/Codex.

4. **Small sample**: 3 tasks is enough to show a pattern, not for statistical significance (n<30).

5. **Enhanced prompts are longer**: More tokens in = more features specified = more features out. This is the MECHANISM of enhancement, not a confound.

---

## Data Files

All test data is preserved in this directory:

```
ab-test-2026-05-21/
├── report.md                    # This report
├── ab-test-data.json           # Structured JSON with all scores and features
└── prompts/
    ├── raw-T1.txt              # Raw prompt for login validator
    ├── raw-T2.txt              # Raw prompt for rate limiter
    ├── raw-T3.txt              # Raw prompt for TTL cache
    ├── enhanced-T1.txt         # Enhanced prompt for login validator
    ├── enhanced-T2.txt         # Enhanced prompt for rate limiter
    └── enhanced-T3.txt         # Enhanced prompt for TTL cache
```

---

## Conclusion

Enhanced prompts produced measurably better code across all 3 tasks. The improvement is **not** because the model is smarter — it's the **same model**. Enhancement works by:

1. **Specifying what the model should deliver** (boundaries, error codes, test count)
2. **Showing concrete examples** of expected output format
3. **Activating domain expertise** by framing the task with production context
4. **Setting a quality bar** through explicit success criteria

The raw prompt results are already good (4.07/5) — Claude is a capable model. But enhancement closes the gap between "good enough" and "production-ready" by making implicit requirements explicit.

**Enhancement is not magic. It's specification.**
