# Workload 05: Debug Task

## Prompt

```
这个函数有 bug，帮我找出来并修复：

def average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

# 测试：average([]) 会崩溃
```

## Expected Behavior

1. Agent identifies the bug (division by zero for empty list)
2. Agent presents checkpoint with bug description
3. If "Continue" → Agent provides fix
4. Checkpoint again
5. User "Done"

## Interaction Script

```
User: [prompt]
Agent: [identifies ZeroDivisionError] → checkpoint
User: "Continue"
Agent: [adds len check or guard] → checkpoint
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
    r'ZeroDivision|empty|空列表|除零',  # bug identified
]
```

## Checkpoints Expected

- After bug identification: 1
- After fix: 1
- Total: 2 minimum
