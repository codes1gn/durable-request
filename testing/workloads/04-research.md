# Workload 04: Research/Analysis Task

## Prompt

```
分析这段代码的性能问题，给出优化建议：

def find_duplicates(lst):
    duplicates = []
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] == lst[j] and lst[i] not in duplicates:
                duplicates.append(lst[i])
    return duplicates
```

## Expected Behavior

1. Agent analyzes the code, identifies O(n²) complexity
2. Agent presents checkpoint with analysis summary
3. If user "Continue" → Agent provides optimized version
4. Checkpoint again
5. User "Done"

## Interaction Script

```
User: [prompt]
Agent: [analysis: O(n²), nested loops, etc] → checkpoint
User: "Continue"
Agent: [optimized version with set/Counter] → checkpoint
User: "Done"
Agent: [ends]
```

## Features Tested

- F1: Checkpoint after task completion
- F2: TodoWrite + AskQuestion in same batch
- F4: Task summary in prompt
- F10: No silent completion

## Verification Patterns

```python
patterns = [
    r'TodoWrite.*durable-checkpoint.*in_progress',
    r'AskQuestion',
    r'O\(n²\)|O\(n\^2\)|nested|复杂度',  # analysis content
]
```

## Checkpoints Expected

- After analysis: 1
- After optimization: 1
- Total: 2 minimum
