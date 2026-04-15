import { motion } from "framer-motion";
import { ScrollReveal } from "../components/ScrollReveal";
import { CodeEditor } from "../components/CodeEditor";
import screenshot1 from "../assets/企业微信截图_17762224642747.png";
import screenshot2 from "../assets/企业微信截图_17762225008593.png";
import screenshot3 from "../assets/企业微信截图_17762225117563.png";
import screenshot4 from "../assets/企业微信截图_17762225579946.png";
import screenshot5 from "../assets/企业微信截图_17762225739321.png";

const userSteps = [
  {
    num: "01",
    title: "Press Ctrl+Shift+S — input box appears",
    desc: "While the agent is working, press Ctrl+Shift+S (or Cmd+Shift+S on Mac). A lightweight input box appears inline. Type your instruction and press Enter to queue it.",
    color: "text-amber-400",
    bg: "bg-amber-500/10",
    screenshot: screenshot2,
    screenshotAlt: "Steering message input box prompt",
    caption: "The input box appears immediately — type and press Enter to send",
  },
  {
    num: "02",
    title: "Message queued — notification confirms",
    desc: "A toast notification confirms the message is queued. The agent has not been interrupted — it keeps running and will see your message at its next Shell tool call.",
    color: "text-orange-400",
    bg: "bg-orange-500/10",
    screenshot: screenshot3,
    screenshotAlt: "Steering queued notification toast",
    caption: "Instant confirmation; agent continues without interruption",
  },
  {
    num: "03",
    title: "Status bar turns yellow — message pending",
    desc: "The ⚡ Steer button in the status bar turns yellow and shows your queued message. It stays yellow until the hook delivers the message to the agent — no blinking, no timeout.",
    color: "text-yellow-400",
    bg: "bg-yellow-500/10",
    screenshot: screenshot4,
    screenshotAlt: "Yellow Steering status bar button in Cursor IDE",
    caption: "Stationary yellow badge holds until the message is consumed",
  },
  {
    num: "04",
    title: "Agent acknowledges with a bounding box",
    desc: "At the agent's next Shell tool call, the hook injects your message into the tool output. The agent must respond with the mandatory STEERING RECEIVED box — your message verbatim, plus the adjusted plan.",
    color: "text-emerald-400",
    bg: "bg-emerald-500/10",
    screenshot: screenshot5,
    screenshotAlt: "Agent STEERING RECEIVED bounding box acknowledgement",
    caption: "Agent echoes your message and adjusted plan — status bar clears within 1 second",
  },
];

const hookPipeline = `User types: steer "focus on the API layer"
         │
         ▼
~/.durable-request/data/steering-message  (file written)
         │
preToolUse hook watches every tool call
         │
         ▼  (next Shell tool call)
steering-hook.sh reads the file
  → deletes it (consumed)
  → prepends echo '╔══ ⚡ USER STEERING MESSAGE ╚══...' to the Shell command
         │
         ▼
Shell tool output now contains the steering box
  → model WILL see this in the tool result
         │
         ▼
Agent acknowledges with STEERING RECEIVED box
  → describes adjusted plan  
  → continues working within same request`;

const ackBoxExample = `╔══════════════════════════════════════════════════════════════╗
║ ⚡ STEERING RECEIVED                                          ║
╠══════════════════════════════════════════════════════════════╣
║ Message : focus on the API layer                              ║
╠══════════════════════════════════════════════════════════════╣
║ Response: Understood. Pivoting to the API layer now —         ║
║           deprioritising UI changes until you say otherwise.  ║
╚══════════════════════════════════════════════════════════════╝`;

const hookCode = `# steering-hook.sh — preToolUse hook strategy
#
# PROBLEM: Cursor additionalContext / agent_message do NOT surface to model.
# WORKAROUND: For Shell tools, prepend an echo to the command so the steering
# message appears in the tool's stdout — which the model DOES see.

if [ "$TOOL_NAME" = "Shell" ]; then
  # Consume the pending steering message
  rm -f "$STEERING_FILE"

  # Prepend the bounding box echo to the agent's original command
  NEW_COMMAND="echo '╔═══ ⚡ USER STEERING MESSAGE ═══╗
║ $STEERING_MSG
╚══════════════════════════════╝
Please acknowledge and incorporate this instruction.' && $ORIGINAL_COMMAND"

  # Return updated_input so Cursor runs the modified command
  jq -n --arg cmd "$NEW_COMMAND" '{
    "permission": "allow",
    "updated_input": { "command": $cmd }
  }'
fi

# For non-Shell tools: keep the file pending.
# It will be delivered at the next Shell call.`;

const statusBarLogic = `// extension.ts — adaptive polling, no blinking

// BEFORE (broken): 30-second timeout reset state regardless of file
setTimeout(() => checkPendingSteering(), 30000)  // caused flicker

// AFTER (correct): poll the actual file; rate adapts to state
pollInterval = setInterval(() => checkPendingSteering(), 5000)  // idle

function adjustPollRate(pendingNow: boolean) {
  const targetMs = pendingNow ? 1000 : 5000   // 1 s while pending
  if (currentMs !== targetMs) {
    clearInterval(pollInterval)
    pollInterval = setInterval(() => checkPendingSteering(), targetMs)
  }
}

// Button stays yellow until the file is gone (consumed by hook)
// Clears within 1 second of the hook consuming the file`;

export function Steering() {
  return (
    <section className="relative min-h-screen">
      {/* Background decorations */}
      <div className="absolute inset-0 bg-grid opacity-40 dark:opacity-20" />
      <div className="absolute top-1/4 left-1/3 w-[500px] h-[500px] rounded-full bg-amber-400/8 dark:bg-amber-500/5 blur-3xl" />
      <div className="absolute bottom-1/3 right-1/4 w-[400px] h-[400px] rounded-full bg-orange-400/8 dark:bg-orange-500/5 blur-3xl" />

      <div className="relative max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-20">

        {/* ── Hero ── */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-20 text-center"
        >
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border bg-[var(--card)] text-sm mb-6">
            <span className="text-amber-400 text-base">⚡</span>
            <span className="text-[var(--muted-foreground)]">New in v1.2</span>
          </div>
          <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight mb-4">
            In-Continuation Steering
            <span className="block text-amber-400 text-2xl sm:text-3xl font-bold mt-1">
              Free of Request
            </span>
          </h1>
          <p className="text-lg text-[var(--muted-foreground)] max-w-2xl mx-auto leading-relaxed">
            Redirect the agent mid-task — without interrupting it, and without consuming an
            extra API request. Send a message any time; the hook injects it at the next Shell
            call inside the <em>same conversation</em>, the agent acknowledges visibly, and
            continues with your new direction.
          </p>

        </motion.div>

        {/* ── Platform Compatibility ── */}
        <ScrollReveal delay={0.1}>
          <div className="mb-20">
            <h2 className="text-xl font-bold mb-2 text-center">Market Comparison</h2>
            <p className="text-sm text-[var(--muted-foreground)] text-center mb-6 max-w-2xl mx-auto">
              In-continuation steering is a feature all major AI coding tools have natively — except Cursor.
              Cursor (IDE and CLI) has no official support. durable-request implements it for both, free of request.
            </p>
            <div className="space-y-4 max-w-4xl mx-auto">
              {/* Row 1: Competitors that already had it */}
              <div className="rounded-xl border border-[var(--border)] bg-[var(--card)] p-4">
                <div className="text-xs text-[var(--muted-foreground)] font-semibold mb-3 uppercase tracking-wider">
                  Other tools — already supported
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div className="rounded-lg border border-[var(--border)] bg-[var(--background)] p-4">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-semibold">Claude Code</span>
                      <span className="text-sm font-bold text-emerald-400">✓</span>
                    </div>
                    <div className="text-xs font-mono text-emerald-400 mb-2">Native, free of request</div>
                    <p className="text-xs text-[var(--muted-foreground)]">
                      Built-in steering via AskUserQuestion.
                    </p>
                  </div>
                  <div className="rounded-lg border border-[var(--border)] bg-[var(--background)] p-4">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-semibold">Codex</span>
                      <span className="text-sm font-bold text-emerald-400">✓</span>
                    </div>
                    <div className="text-xs font-mono text-emerald-400 mb-2">Native, free of request</div>
                    <p className="text-xs text-[var(--muted-foreground)]">
                      Shell-level steering built into the runtime.
                    </p>
                  </div>
                  <div className="rounded-lg border border-[var(--border)] bg-[var(--background)] p-4">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-semibold">Copilot IDE</span>
                      <span className="text-sm font-bold text-amber-400">✓</span>
                    </div>
                    <div className="text-xs font-mono text-amber-400 mb-2">Native, +1 request</div>
                    <p className="text-xs text-[var(--muted-foreground)]">
                      Question carousel costs one extra API call per message.
                    </p>
                  </div>
                </div>
              </div>

              {/* Row 2: Cursor — both unsupported officially, both solved by durable-request */}
              <div className="rounded-xl border-2 border-amber-500/40 bg-[var(--card)] p-4">
                <div className="flex items-center gap-3 mb-3">
                  <div className="text-xs text-amber-400 font-semibold uppercase tracking-wider">
                    Cursor (官方不支持)
                  </div>
                  <div className="h-px flex-1 bg-amber-500/20" />
                  <div className="text-xs font-bold px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 uppercase tracking-wider">
                    ✓ durable-request 实现了
                  </div>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div className="rounded-lg border-2 border-emerald-500/40 bg-[var(--background)] p-4 relative">
                    <div className="absolute -top-3 left-3">
                      <span className="text-[10px] font-bold px-2 py-1 rounded-full bg-emerald-500 text-black uppercase tracking-wider shadow">
                        ✓ durable-request
                      </span>
                    </div>
                    <div className="mt-2">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-semibold">Cursor IDE</span>
                        <span className="text-sm font-bold text-emerald-400">✓</span>
                      </div>
                      <div className="text-xs font-mono text-emerald-400 mb-2">Free of request</div>
                      <p className="text-xs text-[var(--muted-foreground)]">
                        VSCode extension injects steering via status bar button + preToolUse Shell injection.
                      </p>
                    </div>
                  </div>
                  <div className="rounded-lg border-2 border-emerald-500/40 bg-[var(--background)] p-4 relative">
                    <div className="absolute -top-3 left-3">
                      <span className="text-[10px] font-bold px-2 py-1 rounded-full bg-emerald-500 text-black uppercase tracking-wider shadow">
                        ✓ durable-request
                      </span>
                    </div>
                    <div className="mt-2">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-semibold">Cursor CLI</span>
                        <span className="text-sm font-bold text-emerald-400">✓</span>
                      </div>
                      <div className="text-xs font-mono text-emerald-400 mb-2">Free of request</div>
                      <p className="text-xs text-[var(--muted-foreground)]">
                        Shell command injection via updated_input — steering in-continuation with zero extra API cost.
                      </p>
                    </div>
                  </div>
                </div>
                <p className="text-xs text-[var(--muted-foreground)] mt-3 text-center">
                  Both Cursor modes lacked official steering support. durable-request implements it for both — free of request.
                </p>
              </div>
            </div>
          </div>
        </ScrollReveal>

        {/* ═══════════════════════════════════════════════
            PART 1: USER VIEW
        ═══════════════════════════════════════════════ */}
        <ScrollReveal>
          <div className="mb-6">
            <h2 className="text-2xl font-bold mb-2">How to Use</h2>
            <p className="text-sm text-[var(--muted-foreground)] mb-10">
              Four steps from your message to the agent's visible acknowledgement.
            </p>
          </div>
        </ScrollReveal>

        <div className="space-y-10 mb-20">
          {userSteps.map((step, i) => (
            <ScrollReveal key={step.num} delay={0.08 * i}>
              <div className="rounded-2xl border bg-[var(--card)] overflow-hidden">
                <div className="flex items-start gap-4 p-6 pb-4">
                  <span className={`text-3xl font-extrabold ${step.color} font-mono shrink-0`}>
                    {step.num}
                  </span>
                  <div>
                    <h3 className="text-lg font-bold mb-1">{step.title}</h3>
                    <p className="text-sm text-[var(--muted-foreground)] leading-relaxed">
                      {step.desc}
                    </p>
                  </div>
                </div>
                {/* Screenshot */}
                <div className="mx-4 mb-4">
                  <div className={`rounded-xl border overflow-hidden shadow-lg ${step.bg}`}>
                    <div className="flex items-center gap-2 px-4 py-2 border-b bg-[#161b22]/60">
                      <div className="flex gap-1.5">
                        <span className="w-2.5 h-2.5 rounded-full bg-red-400/60" />
                        <span className="w-2.5 h-2.5 rounded-full bg-yellow-400/60" />
                        <span className="w-2.5 h-2.5 rounded-full bg-green-400/60" />
                      </div>
                      <span className={`text-[10px] font-mono ml-2 opacity-60 ${step.color}`}>
                        Cursor IDE
                      </span>
                    </div>
                    <div className="flex justify-center bg-[#0d1117] px-4 py-3">
                      <img
                        src={step.screenshot}
                        alt={step.screenshotAlt}
                        className="max-h-40 w-auto object-contain"
                        style={{ imageRendering: "auto" }}
                      />
                    </div>
                  </div>
                  <p className="text-center text-xs text-[var(--muted-foreground)] mt-2">
                    {step.caption}
                  </p>
                </div>
              </div>
            </ScrollReveal>
          ))}
        </div>

        {/* Real conversation screenshot — the E2E test */}
        <ScrollReveal delay={0.1}>
          <div className="mb-20">
            <h3 className="text-lg font-bold mb-2 text-center">
              Live end-to-end verification
            </h3>
            <p className="text-sm text-[var(--muted-foreground)] text-center mb-6 max-w-xl mx-auto">
              This screenshot was captured during the first live E2E test in this repo. The user
              sent <code className="px-1 py-0.5 rounded bg-[var(--muted)] text-xs font-mono">can you see this message</code> via the status bar button; the
              hook injected it into the agent's Shell output and the agent responded with the full bounding box.
            </p>
            <div className="max-w-3xl mx-auto">
              <div className="rounded-xl border-2 border-amber-500/30 overflow-hidden shadow-2xl shadow-amber-500/10">
                <div className="flex items-center gap-2 px-4 py-2 border-b border-amber-500/20 bg-[#161b22]">
                  <div className="flex gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-red-400/80" />
                    <span className="w-2.5 h-2.5 rounded-full bg-yellow-400/80" />
                    <span className="w-2.5 h-2.5 rounded-full bg-green-400/80" />
                  </div>
                  <span className="text-[10px] text-amber-400/70 ml-2 font-mono">
                    live E2E test — hook injection + agent acknowledgement
                  </span>
                </div>
                <div className="flex justify-center bg-[#0d1117] px-4 py-4">
                  <img
                    src={screenshot1}
                    alt="Live end-to-end test: STEERING RECEIVED bounding box in agent response"
                    className="max-h-64 w-auto object-contain"
                  />
                </div>
              </div>
              <p className="text-center text-xs text-[var(--muted-foreground)] mt-2">
                The agent's reply shows the full bounding box — message verbatim + adjusted plan
              </p>
            </div>
          </div>
        </ScrollReveal>

        {/* ═══════════════════════════════════════════════
            PART 2: SYSTEM DESIGN
        ═══════════════════════════════════════════════ */}
        <ScrollReveal>
          <div className="mb-6">
            <h2 className="text-2xl font-bold mb-2">System Design</h2>
            <p className="text-sm text-[var(--muted-foreground)] mb-10">
              How the three-layer pipeline delivers your message reliably without interrupting the agent.
            </p>
          </div>
        </ScrollReveal>

        {/* Pipeline overview */}
        <ScrollReveal delay={0.05}>
          <div className="mb-12">
            <h3 className="text-lg font-bold mb-4">End-to-End Pipeline</h3>
            <CodeEditor filename="steering-pipeline.txt">
              <pre className="text-[var(--foreground)] text-xs sm:text-sm leading-relaxed font-mono whitespace-pre">
                <code>{hookPipeline}</code>
              </pre>
            </CodeEditor>
          </div>
        </ScrollReveal>

        {/* Key design decisions */}
        <div className="mb-12 grid grid-cols-1 sm:grid-cols-2 gap-6">
          {[
            {
              title: "Why file-based IPC?",
              color: "text-amber-400",
              border: "border-amber-500/20",
              points: [
                "Works across all processes — no shared memory needed",
                "Persists across agent restarts and slow Shell calls",
                "Cheap atomic write: echo → rename ensures no partial reads",
                "Status bar polls the file directly — no additional IPC channel",
              ],
            },
            {
              title: "Why Shell-tool injection?",
              color: "text-orange-400",
              border: "border-orange-500/20",
              points: [
                "Cursor additionalContext does NOT surface to the model (bug, March 2026)",
                "agent_message and postToolUse context also suppressed",
                "Shell stdout IS visible to the model as part of the tool result",
                "updated_input.command lets the hook prepend the echo before running",
              ],
            },
            {
              title: "Why mandatory bounding box?",
              color: "text-yellow-400",
              border: "border-yellow-500/20",
              points: [
                "A plain text acknowledgement is easy to miss or skip",
                "The box forces a machine-checkable, human-scannable structure",
                "Pattern F8b in the test suite verifies presence automatically",
                "Placed at top of reply so it can't be buried in long output",
              ],
            },
            {
              title: "Why non-Shell tools keep the file?",
              color: "text-emerald-400",
              border: "border-emerald-500/20",
              points: [
                "Read / Write / Grep tools don't produce stdout the model sees",
                "Consuming the file there would discard the message silently",
                "File stays pending until the next Shell call delivers it correctly",
                "Adaptive 1-second poll ensures the status bar clears promptly after",
              ],
            },
          ].map((card) => (
            <ScrollReveal key={card.title} delay={0.05}>
              <div className={`rounded-xl border ${card.border} bg-[var(--card)] p-5 h-full`}>
                <h4 className={`text-sm font-bold mb-3 ${card.color}`}>{card.title}</h4>
                <ul className="space-y-2">
                  {card.points.map((pt) => (
                    <li key={pt} className="flex items-start gap-2 text-xs text-[var(--muted-foreground)] leading-relaxed">
                      <span className={`mt-0.5 shrink-0 ${card.color}`}>▸</span>
                      {pt}
                    </li>
                  ))}
                </ul>
              </div>
            </ScrollReveal>
          ))}
        </div>

        {/* Hook implementation */}
        <ScrollReveal delay={0.1}>
          <div className="mb-12">
            <h3 className="text-lg font-bold mb-4">
              Hook Implementation
              <span className="ml-2 text-xs font-normal text-[var(--muted-foreground)]">
                steering-hook.sh (preToolUse)
              </span>
            </h3>
            <CodeEditor filename="steering-hook.sh">
              <pre className="text-[var(--foreground)] text-xs sm:text-sm leading-relaxed font-mono">
                <code>{hookCode}</code>
              </pre>
            </CodeEditor>
          </div>
        </ScrollReveal>

        {/* Agent acknowledgement format */}
        <ScrollReveal delay={0.1}>
          <div className="mb-12">
            <h3 className="text-lg font-bold mb-2">
              Agent Acknowledgement Format
            </h3>
            <p className="text-sm text-[var(--muted-foreground)] mb-4">
              The SKILL.md instructs the agent to output this exact structure. The bounding box
              is placed at the very top of the reply, before any other content.
            </p>
            <CodeEditor filename="STEERING RECEIVED (agent reply)">
              <pre className="text-[var(--foreground)] text-sm leading-relaxed font-mono">
                <code>{ackBoxExample}</code>
              </pre>
            </CodeEditor>
          </div>
        </ScrollReveal>

        {/* Status bar fix */}
        <ScrollReveal delay={0.1}>
          <div className="mb-12">
            <h3 className="text-lg font-bold mb-2">
              Stationary Status Bar
              <span className="ml-2 text-xs font-normal text-[var(--muted-foreground)]">
                extension.ts — adaptive polling
              </span>
            </h3>
            <p className="text-sm text-[var(--muted-foreground)] mb-4">
              The previous implementation used a 30-second timeout to reset the button state — causing
              it to blink off even if the message hadn't been consumed. The fix: derive state solely
              from the file, with adaptive poll rate.
            </p>
            <CodeEditor filename="extension.ts">
              <pre className="text-[var(--foreground)] text-xs sm:text-sm leading-relaxed font-mono">
                <code>{statusBarLogic}</code>
              </pre>
            </CodeEditor>
          </div>
        </ScrollReveal>

        {/* Test coverage */}
        <ScrollReveal delay={0.15}>
          <div className="rounded-2xl border bg-[var(--card)] p-6">
            <h3 className="text-lg font-bold mb-4">Test Coverage (v1.2)</h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {[
                {
                  id: "F8",
                  name: "Steering ACK",
                  desc: "Box header ⚡ STEERING RECEIVED present",
                  color: "text-amber-400",
                  status: "✓",
                },
                {
                  id: "F8a",
                  name: "Shell Injection",
                  desc: "USER STEERING MESSAGE visible in Shell output",
                  color: "text-orange-400",
                  status: "✓",
                },
                {
                  id: "F8b",
                  name: "Bounding Box",
                  desc: "Full box with Message + Response rows verified",
                  color: "text-yellow-400",
                  status: "✓",
                },
              ].map((f) => (
                <div key={f.id} className="rounded-xl border bg-[var(--background)] p-4">
                  <div className="flex items-center justify-between mb-1">
                    <span className={`text-sm font-mono font-bold ${f.color}`}>{f.id}</span>
                    <span className="text-emerald-400 text-sm font-bold">{f.status}</span>
                  </div>
                  <div className="text-sm font-semibold mb-0.5">{f.name}</div>
                  <div className="text-xs text-[var(--muted-foreground)]">{f.desc}</div>
                </div>
              ))}
            </div>
            <p className="text-xs text-[var(--muted-foreground)] mt-4 text-center">
              Pattern matching runs via{" "}
              <code className="px-1 py-0.5 rounded bg-[var(--muted)] font-mono">
                testing/scripts/analyze.py
              </code>{" "}
              on all workload transcripts — 10/10 workloads pass on baseline run
            </p>
          </div>
        </ScrollReveal>
      </div>
    </section>
  );
}
