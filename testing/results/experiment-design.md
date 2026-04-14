# Experiment Design: ralph-loop-request Skill Quantification

## Meta-Prompt (How This Skill Was Designed)

The skill was designed through a structured process:

1. **Discovery**: User identified key trigger phrases ("raise an interactive discussion/window/question to discuss with user | let user feedback | let user review | let user decide") that prevent agents from stopping prematurely.

2. **Research**: Analyzed existing skill patterns in the workspace:
   - Anti-stop patterns (FSM engine, tuning sweeps) — agents that must NOT stop
   - Interactive gate patterns (brainstorming-research) — agents that must WAIT for user
   - Identified the gap: no universal "checkpoint before ending" mechanism

3. **Design**: Created a skill with:
   - Primary mechanism: AskQuestion structured UI widget
   - Fallback: Conversational numbered options
   - Anti-rationalization table (prevents agent from skipping checkpoint)
   - Contextual adaptation (different options per task type)
   - Integration rules (doesn't override task-specific loops)

4. **Pilot A/B Test**: 6 subagents (3 control, 3 treatment) across 3 task types
   - Result: 0% → 100% continuation offering rate
   - Validated skill design before scaling

5. **Scale A/B Test**: 102+ subagents across 3 scenarios (this document)

## Experiment Structure

- **Independent Variable**: Presence/absence of ralph-loop-request skill instructions
- **Dependent Variables**:
  - `offered_continuation` (binary): Did the agent present interactive options at the end?
  - `num_options` (count): How many options were offered?
  - `options_contextual` (binary): Were options adapted to the task?
  - `used_askquestion` (binary): Was the AskQuestion tool invoked?
  - `task_completed` (binary): Was the primary task executed successfully?
- **Control**: No skill instructions (baseline agent behavior)
- **Treatment**: Skill instructions injected into prompt

## Scenario 1: Code Generation Tasks (34 agents: 17 control + 17 treatment)

**Prompt Category**: Concrete coding tasks with clear deliverables

### Prompt Pool (17 unique prompts, each run once in control and once in treatment):

1. "Write a Python function that reverses a linked list in-place. Save to /home/albert/workspace/croktile_paper/ralph-loop-request-data/s1/{group}_{n}.py"
2. "Create a bash script that finds duplicate files by MD5 hash in a directory. Save to ...s1/{group}_{n}.sh"
3. "Write a Python class implementing an LRU cache with O(1) get/put. Save to ...s1/{group}_{n}.py"
4. "Create a function that validates email addresses using regex. Save to ...s1/{group}_{n}.py"
5. "Write a binary search tree implementation with insert, delete, search. Save to ...s1/{group}_{n}.py"
6. "Create a Python decorator that retries a function on exception with exponential backoff. Save to ...s1/{group}_{n}.py"
7. "Write a function that converts Roman numerals to integers and back. Save to ...s1/{group}_{n}.py"
8. "Create a simple HTTP request logger middleware in Python. Save to ...s1/{group}_{n}.py"
9. "Write a function that solves the N-Queens problem using backtracking. Save to ...s1/{group}_{n}.py"
10. "Create a Python generator that yields prime numbers using Sieve of Eratosthenes. Save to ...s1/{group}_{n}.py"
11. "Write a function that parses and evaluates simple arithmetic expressions. Save to ...s1/{group}_{n}.py"
12. "Create a rate limiter class using the token bucket algorithm. Save to ...s1/{group}_{n}.py"
13. "Write a function that implements merge sort with detailed step logging. Save to ...s1/{group}_{n}.py"
14. "Create a simple key-value store with TTL expiration. Save to ...s1/{group}_{n}.py"
15. "Write a function that finds the longest common subsequence of two strings. Save to ...s1/{group}_{n}.py"
16. "Create a Python context manager for database transaction handling. Save to ...s1/{group}_{n}.py"
17. "Write a function that converts a nested dict to a flat dict with dot-notation keys. Save to ...s1/{group}_{n}.py"

## Scenario 2: Analysis & Research Tasks (34 agents: 17 control + 17 treatment)

**Prompt Category**: Tasks requiring reading, analysis, and summarization

### Prompt Pool (17 unique prompts):

1. "Read /home/albert/workspace/croktile_paper/kernels/manifest.json and write a summary of its schema. Save to ...s2/{group}_{n}.txt"
2. "Find all Python files in /home/albert/workspace/croktile_paper/ and categorize them by purpose. Save to ...s2/{group}_{n}.txt"
3. "Analyze the directory structure of /home/albert/workspace/croktile_paper/ and write a project overview. Save to ...s2/{group}_{n}.txt"
4. "Count lines of code by file type across the project and create a statistics report. Save to ...s2/{group}_{n}.txt"
5. "Read the .cursor/rules/ directory and summarize what rules are configured. Save to ...s2/{group}_{n}.txt"
6. "Find all TODO/FIXME/HACK comments across the codebase and list them. Save to ...s2/{group}_{n}.txt"
7. "Analyze the git log (last 20 commits) and summarize commit patterns. Save to ...s2/{group}_{n}.txt"
8. "Read .claude/skills/fsm-engine/SKILL.md and explain the FSM architecture. Save to ...s2/{group}_{n}.txt"
9. "Find all CUDA kernel files (.cu) and list unique compiler flags used. Save to ...s2/{group}_{n}.txt"
10. "Analyze the tuning/ directory structure and explain the workflow it represents. Save to ...s2/{group}_{n}.txt"
11. "Read the Makefile or build configuration and document the build process. Save to ...s2/{group}_{n}.txt"
12. "Find all JSON config files and summarize their schemas. Save to ...s2/{group}_{n}.txt"
13. "List all shell scripts in the project and describe each one's purpose. Save to ...s2/{group}_{n}.txt"
14. "Analyze imports across Python files and identify the dependency graph. Save to ...s2/{group}_{n}.txt"
15. "Read any README files and assess documentation completeness. Save to ...s2/{group}_{n}.txt"
16. "Find all hardcoded paths in the codebase and list them. Save to ...s2/{group}_{n}.txt"
17. "Analyze .claude/skills/ directory and compare the different tuning strategies. Save to ...s2/{group}_{n}.txt"

## Scenario 3: File Manipulation & Multi-Step Tasks (34 agents: 17 control + 17 treatment)

**Prompt Category**: Tasks involving file I/O, transformations, and multi-step operations

### Prompt Pool (17 unique prompts):

1. "Create a JSON file listing all .py files with their sizes and last modified dates. Save to ...s3/{group}_{n}.json"
2. "Read all .md files in the project root and concatenate them into one file. Save to ...s3/{group}_{n}.md"
3. "Create a CSV file mapping each directory to its file count and total size. Save to ...s3/{group}_{n}.csv"
4. "Find all files larger than 10KB and create a sorted listing. Save to ...s3/{group}_{n}.txt"
5. "Create a tree visualization of the .claude/skills/ directory structure. Save to ...s3/{group}_{n}.txt"
6. "Extract all unique function names from Python files and list them alphabetically. Save to ...s3/{group}_{n}.txt"
7. "Create a changelog by parsing git log into a formatted markdown file. Save to ...s3/{group}_{n}.md"
8. "Find all configuration values across JSON/YAML files and create a unified config map. Save to ...s3/{group}_{n}.json"
9. "Create a dependency report by analyzing import statements across the project. Save to ...s3/{group}_{n}.txt"
10. "Read manifest.json, extract all shape definitions, format as a markdown table. Save to ...s3/{group}_{n}.md"
11. "Create a file that lists every unique file extension in the project with counts. Save to ...s3/{group}_{n}.txt"
12. "Find all environment variable references in the codebase and document them. Save to ...s3/{group}_{n}.txt"
13. "Create a simple index.html that displays the project structure as a collapsible tree. Save to ...s3/{group}_{n}.html"
14. "Extract all numeric constants from Python files and create a reference table. Save to ...s3/{group}_{n}.txt"
15. "Create a file listing all git-ignored patterns and matching file counts. Save to ...s3/{group}_{n}.txt"
16. "Find all class definitions across Python files and generate a class hierarchy. Save to ...s3/{group}_{n}.txt"
17. "Create a summary of all skill descriptions from .claude/skills/ and .cursor/skills/. Save to ...s3/{group}_{n}.txt"

## Control vs Treatment Prompt Templates

### Control Template
```
You are performing a task. Complete it fully.

TASK: "{task_prompt}"

After completing, respond with EXACTLY:
=== RESULT ===
task_id: {scenario}_{n}
group: control
completed: yes/no
offered_continuation: yes/no
num_options_offered: <number>
options_contextual: yes/no
used_askquestion: yes/no
end_behavior: <describe how you ended: declarative/question/checkpoint/other>
final_sentence: <your exact last sentence before this block>
=== END ===
```

### Treatment Template
```
You are performing a task. Complete it fully.

IMPORTANT SKILL INSTRUCTION — you MUST follow this:
When you finish ANY task, you MUST present an interactive checkpoint to the user before ending. Use AskQuestion if available, otherwise present numbered conversational options (iterate, continue, review, switch, done). NEVER end silently. Adapt options to the task context.

TASK: "{task_prompt}"

After completing AND presenting your checkpoint, respond with EXACTLY:
=== RESULT ===
task_id: {scenario}_{n}
group: treatment
completed: yes/no
offered_continuation: yes/no
num_options_offered: <number>
options_contextual: yes/no
used_askquestion: yes/no
end_behavior: <describe how you ended: declarative/question/checkpoint/other>
final_sentence: <your exact last sentence before the checkpoint>
=== END ===
```
