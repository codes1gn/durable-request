# Control vs treatment (`all-results.jsonl`)

Aggregates from `/home/albert/durable-request/data/all-results.jsonl` (51 control + 51 treatment runs, 102 rows total).

| Metric | Control | Treatment |
| --- | --- | --- |
| Completion rate | 100% (51/51) | 100% (51/51) |
| Continuation rate | 0% (0/51) | 100% (51/51) |
| Avg options offered | 0.0 | 5.0 |
| Contextual options rate | 0% (0/51) | 100% (51/51) |

**Definitions (from JSON fields):** completion = `completed`; continuation = `offered_continuation`; avg options = mean of `num_options_offered`; contextual rate = share with `options_contextual` true.
