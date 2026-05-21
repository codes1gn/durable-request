---
name: enhance-me
author: durable-request
description: "ACTION-FORCING prompt enhancer router. Detects /enhance-me → launches Task subagent → displays enhanced prompt → executes it. Reading this skill without launching a subagent is a protocol violation."
---

# /enhance-me — Prompt Enhancer Router

## The Number One Rule

**YOU MUST LAUNCH A TASK SUBAGENT. YOU MUST DISPLAY THE ENHANCED PROMPT. YOU MUST EXECUTE IT.**

Reading this skill and then responding conversationally — without calling the Task tool, without showing the enhanced prompt in a code fence, or without executing it — is a **protocol violation**. Your turn is incomplete until all three actions occur in sequence.

**Forbidden outcomes:**
- Responding with "I read the enhance-me skill" or any summary without action
- Enhancing the prompt inline (in your own response) without a subagent
- Launching the subagent but not displaying its result to the user
- Displaying the result but not executing it
- Using the wrong skill prefix (e.g. `/enhance-gpt` when routing should be Claude)
- Re-applying `/enhance-me` to the enhanced prompt (infinite recursion)

## Trigger Detection

This skill activates when the user message contains `/enhance-me` anywhere in the text.

## Model Routing Rules

| User writes | Target model | Subagent prompt prefix |
|------------|--------------|----------------------|
| `/enhance-me <task>` | Claude | `/enhance-claude` |
| `/enhance-me claude <task>` | Claude | `/enhance-claude` |
| `/enhance-me gpt <task>` | GPT/Codex | `/enhance-gpt` |
| `<task> /enhance-me` | Claude | `/enhance-claude` |
| `<task> /enhance-me gpt` | GPT/Codex | `/enhance-gpt` |
| `<task> /enhance-me claude` | Claude | `/enhance-claude` |

**Default:** Claude. Only route to GPT when `gpt` appears adjacent to `/enhance-me`.

## Mandatory Protocol — DO NOT SKIP ANY STEP

### Step 1: Extract task text

Strip `/enhance-me` and any model token (`gpt` or `claude`) from the user message. Everything remaining is the raw task.

Example: `/enhance-me gpt Add retry logic to the API client`
→ Model: `gpt`
→ Task: `Add retry logic to the API client`

### Step 2: Determine target model

Apply the routing table above. If ambiguous, default to `claude`.

### Step 3: CALL THE TASK TOOL — IMMEDIATELY

Do not think about it. Do not explain what you're about to do. **Call the Task tool now:**

```
Task({
  description: "Enhance prompt for <claude|gpt>",
  subagent_type: "generalPurpose",
  prompt: "/enhance-<claude|gpt> <extracted task text>"
})
```

**Concrete examples:**

For `/enhance-me Add dark mode`:
```
Task({
  description: "Enhance prompt for claude",
  subagent_type: "generalPurpose",
  prompt: "/enhance-claude Add dark mode"
})
```

For `/enhance-me gpt Fix the auth flow`:
```
Task({
  description: "Enhance prompt for gpt",
  subagent_type: "generalPurpose",
  prompt: "/enhance-gpt Fix the auth flow"
})
```

The subagent will load the corresponding skill (`enhance-claude` or `enhance-gpt`), transform the raw task, and return the enhanced prompt as its response.

### Step 4: DISPLAY the enhanced prompt — FULL TEXT, NOT A SUMMARY

After the Task subagent returns, you MUST display its **entire output** in your response using this exact format:

```
**Enhanced prompt (<Claude|GPT>):**

\```
<full enhanced prompt text from subagent — every line, no truncation>
\```
```

This is mandatory because:
- The user must be able to review what was generated
- It must be visible in chat history for future reference
- The main agent must see it to execute it correctly

**Do NOT summarize, paraphrase, or truncate.** Show the full text.

### Step 5: EXECUTE the enhanced prompt

Take the enhanced prompt and execute it as your working instructions. This means:
- If it asks you to write code → write the code
- If it asks you to analyze something → do the analysis
- If it asks you to plan → produce the plan

**Do NOT re-apply `/enhance-me`.** The prompt is already enhanced. Execute it directly.

## Why Subagent (Not Inline Enhancement)

- Subagent has dedicated context for enhancement best practices (XML structuring, primacy/recency, role framing, examples)
- Main agent stays focused on execution rather than meta-prompting
- Clean separation: enhancement skill evolves independently
- User sees the enhanced prompt explicitly (transparency)
- Same request, same session — no extra API cost

## Protocol Compliance Check

Before ending your turn after `/enhance-me` triggers, verify:

- [ ] Task subagent was called (not just read about)
- [ ] Correct model skill was used (`/enhance-claude` or `/enhance-gpt`)
- [ ] Full enhanced prompt was displayed in a code fence
- [ ] Enhanced prompt was executed (work was done)

If any box is unchecked, your turn is incomplete. Go back and complete the missing step.
