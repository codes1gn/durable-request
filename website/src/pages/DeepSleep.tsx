import { motion } from "framer-motion";
import { ScrollReveal } from "../components/ScrollReveal";
import { CodeEditor } from "../components/CodeEditor";
import screenshot1 from "../assets/企业微信截图_17792676317810.png";
import screenshot2 from "../assets/企业微信截图_17793357497952.png";
import screenshot3 from "../assets/企业微信截图_17793359484857.png";
import screenshot4 from "../assets/企业微信截图_17793424452750.png";

const howItWorksSteps = [
  {
    num: "01",
    title: "User asks agent to sleep",
    desc: "At any checkpoint, just say 'sleep' or '/deep-sleep'. The agent enters deep-sleep mode — a real Shell process that polls for a wake signal every 5 seconds.",
    color: "text-cyan-400",
    screenshot: screenshot2,
    screenshotAlt: "Agent entering deep-sleep mode with keep-alive terminal messages",
    caption: "Agent enters deep-sleep mode — terminal shows keep-alive messages",
    imgClass: "max-h-80",
  },
  {
    num: "02",
    title: "User returns and wakes the agent",
    desc: "Two ways to wake: touch the wake file, or kill the deep-sleep process. The terminal's stop button also works. Within 5 seconds the agent resumes.",
    color: "text-blue-400",
    screenshot: screenshot4,
    screenshotAlt: "Split view: checkpoint UI and user killing deep-sleep process",
    caption: "Left: checkpoint UI ready | Right: user kills deep-sleep process to wake agent",
    imgClass: "max-h-96",
  },
  {
    num: "03",
    title: "Agent resumes with full context",
    desc: "The agent picks up exactly where it left off. No re-prompting, no context loss. It even tells you how long the sleep lasted.",
    color: "text-emerald-400",
    screenshot: screenshot3,
    screenshotAlt: "Agent woke up after 9 minutes with AskQuestion checkpoint",
    caption: "Agent woke up after 9 minutes and immediately presented a checkpoint",
    imgClass: "max-h-96",
  },
];

const wakeCode = `# Method 1: Touch the wake file
touch ~/.cursor/skills/durable-request/.deep-sleep-wake

# Method 2: Kill the process
kill $(pgrep -f deep-sleep.sh)

# Method 3: Click the terminal's stop button in Cursor IDE
# (This sends SIGTERM to the shell, which wakes the agent)

# Agent resumes instantly — no extra request consumed`;

export function DeepSleep() {
  return (
    <section className="relative min-h-screen">
      {/* Background decorations */}
      <div className="absolute inset-0 bg-grid opacity-40 dark:opacity-20" />
      <div className="absolute top-1/4 left-1/3 w-[500px] h-[500px] rounded-full bg-cyan-400/8 dark:bg-cyan-500/5 blur-3xl" />
      <div className="absolute bottom-1/3 right-1/4 w-[400px] h-[400px] rounded-full bg-blue-400/8 dark:bg-blue-500/5 blur-3xl" />

      <div className="relative max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-20">

        {/* ── Hero ── */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-20 text-center"
        >
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border bg-[var(--card)] text-sm mb-6">
            <span className="text-cyan-400 text-base">🌙</span>
            <span className="text-[var(--muted-foreground)]">Session Recovery</span>
          </div>
          <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight mb-4">
            Deep Sleep
            <span className="block text-cyan-400 text-2xl sm:text-3xl font-bold mt-1">
              Never Lose a Session Again
            </span>
          </h1>
          <p className="text-lg text-[var(--muted-foreground)] max-w-2xl mx-auto leading-relaxed">
            When you step away, the agent doesn't have to die. Deep-sleep keeps the session
            alive using a real Shell process — killable anytime, wake-up in 5 seconds, no extra
            request consumed.
          </p>
        </motion.div>

        {/* ── Section 1: The Problem ── */}
        <ScrollReveal delay={0.1}>
          <div className="mb-20">
            <h2 className="text-2xl font-bold mb-2 text-center">The Problem</h2>
            <p className="text-sm text-[var(--muted-foreground)] text-center mb-8 max-w-2xl mx-auto">
              AskQuestion timeouts kill sessions. Deep-sleep replaces fragile prompt-based waiting
              with a real, killable Shell process.
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-4xl mx-auto">
              <div className="rounded-xl border bg-[var(--card)] overflow-hidden">
                <div className="px-4 py-3 border-b bg-red-500/10 flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-full bg-red-500 shrink-0" />
                  <span className="text-sm font-semibold text-[var(--foreground)]">
                    Without deep-sleep
                  </span>
                </div>
                <div className="p-5">
                  <ul className="text-sm text-[var(--muted-foreground)] space-y-2.5">
                    <li className="flex items-start gap-2">
                      <span className="text-red-400 shrink-0 mt-0.5">▸</span>
                      AskQuestion can only wait for a fixed time
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-red-400 shrink-0 mt-0.5">▸</span>
                      If Cursor's timeout triggers, the AskQuestion UI disappears
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-red-400 shrink-0 mt-0.5">▸</span>
                      Session terminates — all context lost
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-red-400 shrink-0 mt-0.5">▸</span>
                      Only option: start a new request and re-explain everything
                    </li>
                  </ul>
                </div>
              </div>
              <div className="rounded-xl border bg-[var(--card)] overflow-hidden">
                <div className="px-4 py-3 border-b bg-emerald-500/10 flex items-center gap-2">
                  <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 shrink-0" />
                  <span className="text-sm font-semibold text-[var(--foreground)]">
                    With deep-sleep
                  </span>
                </div>
                <div className="p-5">
                  <ul className="text-sm text-[var(--muted-foreground)] space-y-2.5">
                    <li className="flex items-start gap-2">
                      <span className="text-emerald-400 shrink-0 mt-0.5">▸</span>
                      Real Shell process blocks the turn indefinitely (up to 2h)
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-emerald-400 shrink-0 mt-0.5">▸</span>
                      Kill the process anytime to wake the agent instantly
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-emerald-400 shrink-0 mt-0.5">▸</span>
                      Even if AskQuestion UI times out, killing deep-sleep resumes the session
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-emerald-400 shrink-0 mt-0.5">▸</span>
                      Agent wakes with full context — no extra request consumed
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </ScrollReveal>

        {/* ── Section 2: How It Works ── */}
        <ScrollReveal>
          <div className="mb-6">
            <h2 className="text-2xl font-bold mb-2">How It Works</h2>
            <p className="text-sm text-[var(--muted-foreground)] mb-10">
              Three steps from saying "sleep" to resuming with full context intact.
            </p>
          </div>
        </ScrollReveal>

        <div className="space-y-10 mb-20">
          {howItWorksSteps.map((step, i) => (
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
                <div className="mx-4 mb-4">
                  <div className="rounded-xl border overflow-hidden shadow-lg">
                    <div className="flex items-center gap-2 px-4 py-2 border-b bg-[#161b22]/60">
                      <div className="flex gap-1.5">
                        <span className="w-2.5 h-2.5 rounded-full bg-red-400/60" />
                        <span className="w-2.5 h-2.5 rounded-full bg-yellow-400/60" />
                        <span className="w-2.5 h-2.5 rounded-full bg-green-400/60" />
                      </div>
                      <span className="text-[10px] font-mono ml-2 opacity-60">Cursor IDE</span>
                    </div>
                    <div className="flex justify-center bg-[#0d1117] px-4 py-3">
                      <img
                        src={step.screenshot}
                        alt={step.screenshotAlt}
                        className={`${step.imgClass} w-auto object-contain`}
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

        {/* ── Section 3: Wake Methods ── */}
        <ScrollReveal delay={0.1}>
          <div className="mb-20">
            <h2 className="text-2xl font-bold mb-2">Wake Methods</h2>
            <p className="text-sm text-[var(--muted-foreground)] mb-6">
              Three ways to wake the agent instantly — no extra request consumed.
            </p>
            <CodeEditor filename="wake-agent.sh">
              <pre className="text-[var(--foreground)] text-xs sm:text-sm leading-relaxed font-mono">
                <code>{wakeCode}</code>
              </pre>
            </CodeEditor>
          </div>
        </ScrollReveal>

        {/* ── Section 4: The Origin Story ── */}
        <ScrollReveal delay={0.1}>
          <div className="mb-20">
            <h2 className="text-2xl font-bold mb-2 text-center">The Origin Story</h2>
            <p className="text-sm text-[var(--muted-foreground)] text-center mb-6 max-w-2xl mx-auto">
              The first time deep-sleep was triggered naturally — a user asked the agent to
              "sleep 19 hours then ask me again". The agent saved all work, said "Good night!",
              and entered deep-sleep mode.
            </p>
            <div className="max-w-3xl mx-auto">
              <div className="rounded-xl border-2 border-cyan-500/30 overflow-hidden shadow-2xl shadow-cyan-500/10">
                <div className="flex items-center gap-2 px-4 py-2 border-b border-cyan-500/20 bg-[#161b22]">
                  <div className="flex gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-red-400/80" />
                    <span className="w-2.5 h-2.5 rounded-full bg-yellow-400/80" />
                    <span className="w-2.5 h-2.5 rounded-full bg-green-400/80" />
                  </div>
                  <span className="text-[10px] text-cyan-400/70 ml-2 font-mono">
                    first natural deep-sleep trigger — "sleep 19 hours then ask me again"
                  </span>
                </div>
                <div className="flex justify-center bg-[#0d1117] px-4 py-4">
                  <img
                    src={screenshot1}
                    alt="User chose sleep 19 hours — agent says Good night after saving work"
                    className="max-h-96 w-auto object-contain"
                  />
                </div>
              </div>
            </div>
          </div>
        </ScrollReveal>

        {/* ── Section 5: Stats ── */}
        <ScrollReveal delay={0.15}>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-2xl mx-auto">
            <div className="rounded-xl border bg-[var(--card)] p-6 text-center">
              <div className="text-4xl font-extrabold text-cyan-400 font-mono">2h</div>
              <div className="text-sm text-[var(--muted-foreground)] mt-2">
                Max sleep time (configurable)
              </div>
            </div>
            <div className="rounded-xl border bg-[var(--card)] p-6 text-center">
              <div className="text-4xl font-extrabold text-blue-400 font-mono">5s</div>
              <div className="text-sm text-[var(--muted-foreground)] mt-2">
                Wake response time
              </div>
            </div>
          </div>
        </ScrollReveal>
      </div>
    </section>
  );
}
