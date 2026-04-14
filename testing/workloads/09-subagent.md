# Workload 09: Subagent Mode

## Prompt

```
[Run as subagent with no AskQuestion tool available]

实现一个简单的 Stack 数据结构，包含 push, pop, peek, is_empty 方法。
```

## Expected Behavior

1. Agent implements Stack class
2. Agent detects no interactive tools available (subagent)
3. Agent uses **conversational fallback** with numbered options
4. Format: "1. Continue\n2. Iterate\n3. Done"
5. User types number or instruction
6. Agent continues or ends

## Interaction Script

```
User: [prompt, as subagent]
Agent: [implements Stack]
       "**Completed:** Stack 实现完成.
        
        What would you like to do next?
        1. Continue
        2. Iterate
        3. Done"
User: "3"
Agent: [ends]
```

## Features Tested

- F7: Subagent conversational fallback

## Verification Patterns

```python
patterns = [
    r'1\.\s*Continue\n2\.\s*Iterate\n3\.\s*Done',  # F7: numbered fallback
    # NOT: AskQuestion (should not be called in subagent)
]
```

## Checkpoints Expected

- After implementation: 1 (conversational)
- Total: 1 minimum

## Special Setup

This workload must be run as a subagent (Task tool) where AskQuestion is not available.
