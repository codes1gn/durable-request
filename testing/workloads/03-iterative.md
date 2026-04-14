# Workload 03: Iterative Refinement

## Prompt

```
写一个 Python 函数实现 FizzBuzz。我会多次迭代优化它。
```

## Expected Behavior

1. Agent implements basic FizzBuzz → checkpoint
2. User: "Iterate - 用 list comprehension 重写"
3. Agent refines → checkpoint
4. User: "Iterate - 加上类型注解"
5. Agent refines → checkpoint
6. User: "Done"

## Interaction Script

```
User: [prompt]
Agent: [basic impl] → checkpoint
User: "用 list comprehension 重写"
Agent: [list comp version] → checkpoint
User: "加上类型注解"
Agent: [typed version] → checkpoint
User: "Done"
Agent: [ends]
```

## Features Tested

- F3: 4 fixed options
- F5: Multi-step checkpoint loop
- F6: Durable loop (continue until Done)

## Verification Patterns

```python
patterns = [
    r'AskQuestion',  # checkpoint present
    r'"Continue".*"Iterate".*"Done"',  # F3
    # Count: >= 3 checkpoints
]
```

## Checkpoints Expected

- Initial: 1
- After 1st iterate: 1
- After 2nd iterate: 1
- Total: 3 minimum
