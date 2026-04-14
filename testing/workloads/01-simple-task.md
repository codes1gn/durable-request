# Workload 01: Simple Single-Step Task

## Prompt

```
给下面这个函数加一个 docstring，解释它的功能和参数：

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

## Expected Behavior

1. Agent adds docstring to the function
2. Agent presents checkpoint with:
   - Task summary mentioning "docstring" or "factorial"
   - 4 options: Continue, Iterate, Done, (empty)
3. If user selects "Done" → session ends
4. If user selects "Iterate" → agent refines and checkpoints again

## Interaction Script

```
User: [prompt above]
Agent: [adds docstring] → checkpoint
User: "Iterate" (or "iterate" or "2")
Agent: [refines] → checkpoint
User: "Done" (or "done" or "3")
Agent: [ends]
```

## Features Tested

- F1: Checkpoint after task completion
- F2: TodoWrite + AskQuestion in same batch
- F3: 4 fixed options
- F4: Task summary in prompt
- F10: No silent completion

## Verification Patterns

```python
patterns = [
    r'TodoWrite.*durable-checkpoint.*in_progress',  # F2
    r'AskQuestion',  # F1
    r'"Continue".*"Iterate".*"Done"',  # F3
    r'docstring|factorial',  # F4 - relevant summary
]
```

## Checkpoints Expected

- Initial completion: 1
- After iterate: 1
- Total: 2 minimum
