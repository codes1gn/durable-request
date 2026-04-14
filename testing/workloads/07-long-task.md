# Workload 07: Long Task (Many Todos)

## Prompt

```
创建一个完整的 Python 项目结构，包含：
1. src/ 目录结构
2. tests/ 目录结构
3. setup.py / pyproject.toml
4. README.md
5. .gitignore
6. requirements.txt
7. 一个示例模块
8. 对应的测试文件
9. GitHub Actions CI 配置
10. pre-commit 配置

每完成一个文件告诉我进度。
```

## Expected Behavior

1. Agent creates many files, generating >20 todos
2. At some point, todo cleanup is triggered
3. Checkpoints after each significant step
4. User alternates "Continue" until done

## Interaction Script

```
User: [prompt]
Agent: [creates files 1-3] → checkpoint (todos ~5)
User: "Continue"
Agent: [creates files 4-6] → checkpoint (todos ~10)
User: "Continue"
Agent: [creates files 7-9] → checkpoint (todos ~15)
User: "Continue"
Agent: [creates file 10] → checkpoint (todos >20, cleanup triggered)
User: "Done"
Agent: [ends]
```

## Features Tested

- F1: Checkpoint after task completion
- F9: Todo cleanup at >20 items

## Verification Patterns

```python
patterns = [
    r'AskQuestion',
    r'todo-cleanup\.sh|merge:\s*false',  # F9: cleanup triggered
    # Or: TodoWrite with reduced list after >20
]
```

## Checkpoints Expected

- Multiple intermediate: ~4
- Total: 4+ minimum
