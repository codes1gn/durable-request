# Workload 10: Complex Composite Task

## Prompt

```
创建一个简单的 URL 缩短器：
1. 生成短码的函数 (base62 编码)
2. 存储映射的字典
3. 编码和解码函数
4. 简单的单元测试

我会分步骤验收，每完成一步告诉我。
```

## Expected Behavior

1. Agent implements step 1 → checkpoint
2. User: "Continue" → step 2 → checkpoint
3. User: "Iterate - 短码长度改成 6" → refine → checkpoint
4. User: "Continue" → step 3 → checkpoint
5. User: "Continue" → step 4 (tests) → checkpoint
6. User: "Done"

## Interaction Script

```
User: [prompt]
Agent: [base62 encoding] → checkpoint
User: "Continue"
Agent: [storage dict] → checkpoint
User: "短码长度改成 6"
Agent: [refines length] → checkpoint
User: "Continue"
Agent: [encode/decode functions] → checkpoint
User: "Continue"
Agent: [unit tests] → checkpoint
User: "Done"
Agent: [ends]
```

## Features Tested

- F1: Checkpoint after task completion
- F2: TodoWrite + AskQuestion in same batch
- F3: 4 fixed options
- F4: Task summary in prompt
- F5: Multi-step checkpoint loop
- F6: Durable loop (continue until Done)
- F10: No silent completion

## Verification Patterns

```python
patterns = [
    r'TodoWrite.*durable-checkpoint.*in_progress',  # F2
    r'AskQuestion',  # F1
    r'"Continue".*"Iterate".*"Done"',  # F3
    # Count: >= 5 checkpoints
]
```

## Checkpoints Expected

- After each step: 4
- After iterate: 1
- Total: 5 minimum

## Notes

This is the most comprehensive workload, testing all major features in a single session.
