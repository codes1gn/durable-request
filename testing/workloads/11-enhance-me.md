# Enhance-Me Test Workload

Test cases for evaluating /enhance-me prompt enhancement quality.

## Test Cases

### T01 — Vague coding request
```
add auth to the app
```

### T02 — Specific but unstructured
```
I need a rate limiter for our API endpoints using Redis, make sure it handles edge cases and is tested
```

### T03 — Debugging request
```
why is my react app slow
```

### T04 — Refactoring request
```
clean up the database module
```

### T05 — Feature request with context
```
we need to add pagination to the user list page, currently it loads all users at once which is bad for performance, use the existing Pagination component in src/components/
```

### T06 — Error investigation
```
getting a 500 error on POST /api/checkout
```

### T07 — Documentation request
```
write docs for the new API
```

### T08 — Code review request
```
review this PR and tell me what's wrong
```

### T09 — Architecture decision
```
should we use graphql or rest for the new service
```

### T10 — Multi-step task
```
set up CI/CD for the project, we use GitHub Actions, need to build, test, and deploy to staging and production
```

## Evaluation Metrics

Each enhanced prompt is scored on:

1. **Structure** (1-5): Does it use model-appropriate structuring (XML for Claude, Markdown for GPT)?
2. **Clarity** (1-5): Is the task unambiguous and specific?
3. **Completeness** (1-5): Are success criteria, constraints, and edge cases covered?
4. **Model-fit** (1-5): Does it apply model-specific techniques (recency for Claude, primacy for GPT)?
5. **Actionability** (1-5): Can an agent execute the enhanced prompt without clarification?

## Scoring Rubric

| Score | Meaning |
|-------|---------|
| 5 | Excellent — production-ready, no improvements needed |
| 4 | Good — minor improvements possible |
| 3 | Acceptable — functional but could be tighter |
| 2 | Weak — missing important elements |
| 1 | Poor — barely better than raw input |
