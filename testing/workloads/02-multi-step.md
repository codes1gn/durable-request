# Workload 02: Multi-Step Implementation

## Prompt

```
创建一个简单的 Python TODO list 管理器：
1. TodoItem 数据类 (id, title, done)
2. TodoList 类 (add, remove, mark_done, list_all)
3. 简单的 CLI 接口

不需要持久化，内存存储即可。
```

## Expected Behavior

1. Agent implements step 1 → checkpoint
2. User: "Continue" → Agent implements step 2 → checkpoint
3. User: "Continue" → Agent implements step 3 → checkpoint
4. User: "Done" → session ends

## Interaction Script

```
User: [prompt above]
Agent: [TodoItem class] → checkpoint
User: "Continue"
Agent: [TodoList class] → checkpoint
User: "Continue"  
Agent: [CLI interface] → checkpoint
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
    # F5/F6: count checkpoint occurrences >= 3
]
```

## Checkpoints Expected

- After step 1: 1
- After step 2: 1
- After step 3: 1
- Total: 3 minimum
