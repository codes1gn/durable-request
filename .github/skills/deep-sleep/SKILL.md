---
name: deep-sleep
author: durable-request
description: "/deep-sleep — Keep agent alive while user is away. Enter low-power polling loop that prevents request timeout."
---

# /deep-sleep — Agent Keep-Alive Mode

## Trigger

When the user says `/deep-sleep`, "deep-sleep", "brb", "I'll be back", or indicates they will be away.

## The Rule

**You MUST call `deep-sleep.sh` via the Shell tool. Do not just acknowledge the user is leaving.**

## Protocol

### Step 1: Call deep-sleep.sh

```bash
bash ~/.cursor/skills/durable-request/deep-sleep.sh [timeout_minutes]
```

- Default timeout: 1440 minutes (24 hours)
- Pass a custom timeout if the user specifies one (e.g., "brb 30 min" → `deep-sleep.sh 30`)

### Step 2: Wait for wake

The script blocks, printing `[deep-sleep] Still sleeping... X/Y min elapsed.` every 60 seconds.

The user wakes the agent by running:
```bash
touch ~/.cursor/skills/durable-request/.deep-sleep-wake
```

### Step 3: After waking

When the script returns (wake signal or timeout), you MUST present a new checkpoint to the user using the durable-request protocol.

## When to Use

- User says "brb", "back in X minutes", "going to lunch", etc.
- You've presented a checkpoint and suspect the user has stepped away
- A long-running background task is executing and you need to stay alive

## When NOT to Use

- As a substitute for checkpoints — always checkpoint first
- When the user is actively responding
- In subagents (they should just return results)
