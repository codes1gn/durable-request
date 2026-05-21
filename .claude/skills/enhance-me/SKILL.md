---
name: enhance-me
author: durable-request
description: Enhance user prompts with model-specific best practices. Detects /enhance-me anywhere in prompt, strips it, delegates to subagent with enhance-claude or enhance-gpt skill.
---

# /enhance-me — Prompt Enhancer Router

## Trigger

When the user message contains `/enhance-me` anywhere in the text:

- `/enhance-me <task>` → enhance for Claude (default)
- `/enhance-me gpt <task>` → enhance for GPT/Codex
- `/enhance-me claude <task>` → enhance for Claude
- `<task> /enhance-me` → enhance for Claude (default)
- `<task> /enhance-me gpt` → enhance for GPT/Codex
- `<task> /enhance-me` with `gpt` anywhere nearby → enhance for GPT/Codex

## Protocol

1. **Extract**: Remove `/enhance-me` and any model specifier (`gpt` or `claude`) from the user message. Preserve all other text as the actual task.
2. **Determine model**: Default is `claude`. If `gpt` appears in proximity to `/enhance-me`, target is GPT/Codex.
3. **Delegate**: Launch a subagent via the `Task` tool with the appropriate enhancement skill prefix:
   - For Claude: `/enhance-claude <actual task>`
   - For GPT: `/enhance-gpt <actual task>`
4. **Surface**: The subagent returns the enhanced prompt. **You MUST display the full enhanced prompt to the user** in your response text before executing it. Use a collapsible block or code fence so the user can review what was generated. This ensures the enhanced prompt is visible in chat history.
5. **Execute**: Execute the enhanced prompt directly. Do NOT re-apply `/enhance-me` to avoid recursive enhancement.

## Subagent invocation

Use the Task tool to delegate:

```
Task({
  description: "Enhance prompt for <model>",
  prompt: "/enhance-<model> <actual task text>"
})
```

The subagent will load the corresponding enhancement skill, transform the raw task into an optimally structured prompt, and return the result.

**After receiving the subagent result:**

1. Display the enhanced prompt to the user in a code fence with a brief label (e.g. "Enhanced prompt (Claude):"). This makes it visible and reviewable in chat history.
2. Then execute the enhanced prompt as your working instructions.

## Why subagent?

- Runs within the same request — no extra API cost
- Subagent has full context of the enhancement skill
- Clean separation: enhancement logic lives in dedicated skills
- Main agent stays lean and focused on execution
- Enhanced prompt is surfaced to the user (not hidden in subagent internals)
