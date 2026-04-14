# Control vs treatment (`all-results.jsonl`)

Aggregates over **102** runs (**51** control, **51** treatment), three scenarios × 17 tasks each (`s1_code_generation`, `s2_analysis_research`, `s3_file_manipulation`).

| Metric | Control | Treatment |
| --- | --- | --- |
| **Completion rate** | 100% (51/51) | 100% (51/51) |
| **Continuation rate** | 0% (0/51) | 100% (51/51) |
| **Avg options offered** | 0.0 | 5.0 |
| **Contextual options rate** | 0% (0/51) | 100% (51/51) |

*Source:* `/home/albert/durable-request/data/all-results.jsonl`. Rates are the fraction of rows in each group with `completed` / `offered_continuation` / `options_contextual` true. Avg options is the mean of `num_options_offered`.
