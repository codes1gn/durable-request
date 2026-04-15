# Workload 06: Task with Steering

## Prompt

```
实现一个简单的计算器类，支持加减乘除。

[中途发送 steering: "先只实现加法和减法，其他的之后再加"]
```

## Expected Behavior

1. Agent starts implementing calculator
2. **Steering message injected** during execution
3. Agent acknowledges steering using the **mandatory bounding box** format
4. Agent adjusts scope (only +/-)
5. Checkpoint with adjusted summary
6. User "Done"

## Interaction Script

```
User: [prompt]
[Steering: "先只实现加法和减法，其他的之后再加"]
Agent: [sees steering in Shell output]
       [outputs bounding box]:
         ╔══════════════════════════════════════════════════════════════╗
         ║ ⚡ STEERING RECEIVED                                          ║
         ╠══════════════════════════════════════════════════════════════╣
         ║ Message : 先只实现加法和减法，其他的之后再加                  ║
         ╠══════════════════════════════════════════════════════════════╣
         ║ Response: Understood. Implementing only add/subtract now.    ║
         ╚══════════════════════════════════════════════════════════════╝
       [implements only +/-] → checkpoint
User: "Continue"
Agent: [maybe adds */ later] → checkpoint
User: "Done"
Agent: [ends]
```

## Features Tested

- F1: Checkpoint after task completion
- F8: Steering acknowledgment (box header `⚡ STEERING RECEIVED` present)
- F8a: Steering message visible in Shell output
- F8b: **Mandatory bounding box** in agent reply (full box with Message + Response rows)

## Verification Patterns

```python
patterns = [
    r'AskQuestion',
    r'STEERING RECEIVED',            # F8: bounding box header
    r'USER STEERING MESSAGE|⚡.*STEERING',  # F8a: visible in Shell output
    # F8b: full box with all required rows
    r'╔[═]+╗.*?⚡\s*STEERING RECEIVED.*?╠[═]+╣.*?Message\s*:.*?╠[═]+╣.*?Response\s*:.*?╚[═]+╝',
]
```

## Checkpoints Expected

- After steering-adjusted impl: 1
- After continue: 1
- Total: 2 minimum

## Special Setup

This workload requires:
1. Running `steer "先只实现加法和减法..."` during agent execution
2. Timing: after prompt, before first checkpoint
