import { motion } from "framer-motion";
import { ScrollReveal } from "../components/ScrollReveal";
import { CodeEditor } from "../components/CodeEditor";

const dimensions = [
  { label: "Structure", raw: 4.67, enhanced: 5.0 },
  { label: "Completeness", raw: 3.67, enhanced: 4.67 },
  { label: "Type Safety", raw: 4.67, enhanced: 5.0 },
  { label: "Error Handling", raw: 3.33, enhanced: 4.0 },
  { label: "Testability", raw: 4.0, enhanced: 5.0 },
];

const maxScore = 5;

const usageSteps = [
  {
    num: "1",
    title: "Type /enhance-me before your task",
    desc: "Example: /enhance-me write a rate limiter — the agent detects the prefix and strips it before enhancement.",
    color: "text-purple-400",
    bg: "bg-accent-500/10",
  },
  {
    num: "2",
    title: "Subagent enhances the prompt",
    desc: "A subagent loads enhance-claude or enhance-gpt, restructures with model-specific best practices, and returns the result.",
    color: "text-emerald-400",
    bg: "bg-emerald-500/10",
  },
  {
    num: "3",
    title: "Agent shows the prompt and executes",
    desc: "The enhanced prompt is displayed in chat history for review, then the agent executes it directly.",
    color: "text-green-400",
    bg: "bg-emerald-500/10",
  },
];

const chatExample = `User: /enhance-me write a TTL cache with LRU eviction

Agent: Enhancing prompt for Claude...

Enhanced prompt (Claude):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<task>
  Build a TypeScript TTL cache with LRU eviction...
  <constraints>
    - Max capacity configurable, default 1000
    - Event system: set, get, delete, expire, evict
    - Cache statistics: hits, misses, evictions
    ...
  </constraints>
  <success_criteria>
    - At least 12 test cases
    - dispose() method for cleanup
    ...
  </success_criteria>
</task>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Executing enhanced prompt...
[Agent produces production-grade TTL+LRU cache]`;

export function EnhanceMe() {
  return (
    <section className="relative min-h-screen">
      {/* Background decorations */}
      <div className="absolute inset-0 bg-grid opacity-40 dark:opacity-20" />
      <div className="absolute top-1/4 right-1/3 w-[500px] h-[500px] rounded-full bg-purple-400/8 dark:bg-purple-500/5 blur-3xl" />
      <div className="absolute bottom-1/3 left-1/4 w-[400px] h-[400px] rounded-full bg-emerald-400/8 dark:bg-emerald-500/5 blur-3xl" />

      <div className="relative max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-20">

        {/* ── Hero ── */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-20 text-center"
        >
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border bg-[var(--card)] text-sm mb-6">
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              className="text-purple-400"
            >
              <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z" />
              <path d="M5 3v4" />
              <path d="M19 17v4" />
              <path d="M3 5h4" />
              <path d="M17 19h4" />
            </svg>
            <span className="text-[var(--muted-foreground)]">Prompt Enhancement</span>
          </div>
          <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight mb-4">
            /enhance-me
            <span className="block text-purple-400 text-2xl sm:text-3xl font-bold mt-1">
              Same Model, Better Output
            </span>
          </h1>
          <p className="text-lg text-[var(--muted-foreground)] max-w-2xl mx-auto leading-relaxed">
            Most prompts are underspecified. /enhance-me transforms your raw task into a
            model-optimized prompt using XML structuring for Claude and primacy-optimized headers
            for GPT — then executes it. Same model, dramatically better code.
          </p>
        </motion.div>

        {/* ── Section 1: The Problem ── */}
        <ScrollReveal>
          <div className="mb-20">
            <h2 className="text-2xl font-bold mb-2 text-center">The Problem</h2>
            <p className="text-sm text-[var(--muted-foreground)] text-center mb-8 max-w-xl mx-auto">
              Raw prompts leave critical details implicit. Enhancement makes requirements explicit.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Raw prompt */}
              <div className="rounded-xl border border-[var(--border)] bg-[var(--card)] p-5">
                <div className="flex items-center gap-2 mb-4">
                  <span className="w-2 h-2 rounded-full bg-red-500" />
                  <span className="text-sm font-semibold">Raw prompt</span>
                </div>
                <div className="rounded-lg bg-red-500/10 border border-red-500/20 px-3 py-2 mb-4">
                  <code className="text-xs font-mono text-[var(--foreground)]">
                    "Write a rate limiter for Express.js"
                  </code>
                </div>
                <ul className="space-y-1.5">
                  {[
                    "No max request spec",
                    "No cleanup strategy",
                    "No header format",
                    "No test count expectation",
                  ].map((item) => (
                    <li
                      key={item}
                      className="flex items-start gap-2 text-xs text-[var(--muted-foreground)]"
                    >
                      <span className="text-red-500 mt-0.5 shrink-0">✕</span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>

              {/* Enhanced prompt */}
              <div className="rounded-xl border border-[var(--border)] bg-[var(--card)] p-5">
                <div className="flex items-center gap-2 mb-4">
                  <span className="w-2 h-2 rounded-full bg-emerald-500" />
                  <span className="text-sm font-semibold">Enhanced prompt</span>
                </div>
                <div className="rounded-lg bg-emerald-500/10 border border-emerald-500/20 px-3 py-2 mb-4 font-mono text-[10px] leading-relaxed text-[var(--foreground)]">
                  <span className="text-purple-400">&lt;task&gt;</span> Rate limiter for Express.js
                  <br />
                  <span className="text-purple-400">&lt;constraints&gt;</span> sliding + fixed window,
                  cleanup, headers...
                  <br />
                  <span className="text-purple-400">&lt;success_criteria&gt;</span> 12+ tests, X-RateLimit-* spec...
                  <br />
                  <span className="text-purple-400">&lt;/task&gt;</span>
                </div>
                <ul className="space-y-1.5">
                  {[
                    "Sliding window + fixed window",
                    "Memory cleanup with timer.unref()",
                    "X-RateLimit-* header spec",
                    "12+ test cases required",
                  ].map((item) => (
                    <li
                      key={item}
                      className="flex items-start gap-2 text-xs text-[var(--muted-foreground)]"
                    >
                      <span className="text-emerald-400 mt-0.5 shrink-0">✓</span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </ScrollReveal>

        {/* ── Section 2: A/B Test Results ── */}
        <ScrollReveal delay={0.1}>
          <div className="mb-20">
            <h2 className="text-2xl font-bold mb-2 text-center">A/B Test Results</h2>
            <p className="text-sm text-[var(--muted-foreground)] text-center mb-8 max-w-xl mx-auto">
              Same model, same tasks — raw prompt vs. /enhance-me enhanced prompt (n=3 tasks, 1–5 scale).
            </p>

            <div className="rounded-xl border bg-[var(--card)] overflow-hidden mb-6">
              <div className="px-4 py-3 border-b bg-[var(--muted)] text-xs font-medium text-[var(--muted-foreground)]">
                Code Quality Scores (1–5 scale, n=3 tasks)
              </div>
              <div className="p-5 space-y-4">
                {dimensions.map((dim) => (
                  <div key={dim.label}>
                    <div className="text-xs text-[var(--muted-foreground)] mb-2">{dim.label}</div>
                    <div className="space-y-1.5">
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] w-14 shrink-0 text-[var(--muted-foreground)]">
                          Raw
                        </span>
                        <div className="flex-1 h-3 bg-[var(--muted)] rounded-full overflow-hidden">
                          <div
                            className="h-full bg-accent-500/40 rounded-full"
                            style={{ width: `${(dim.raw / maxScore) * 100}%` }}
                          />
                        </div>
                        <span className="font-mono text-xs w-8 text-right text-[var(--foreground)]">
                          {dim.raw.toFixed(2)}
                        </span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] w-14 shrink-0 text-[var(--muted-foreground)]">
                          Enhanced
                        </span>
                        <div className="flex-1 h-3 bg-[var(--muted)] rounded-full overflow-hidden">
                          <div
                            className="h-full bg-emerald-500 rounded-full"
                            style={{ width: `${(dim.enhanced / maxScore) * 100}%` }}
                          />
                        </div>
                        <span className="font-mono text-xs w-8 text-right font-semibold text-emerald-400">
                          {dim.enhanced.toFixed(2)}
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-3 gap-3">
              <div className="rounded-xl border bg-[var(--card)] p-4 text-center">
                <div className="text-2xl font-bold text-emerald-400">+16.4%</div>
                <div className="text-[10px] text-[var(--muted-foreground)] mt-1">Quality Gain</div>
              </div>
              <div className="rounded-xl border bg-[var(--card)] p-4 text-center">
                <div className="text-2xl font-bold text-emerald-400">+58%</div>
                <div className="text-[10px] text-[var(--muted-foreground)] mt-1">More Tests</div>
              </div>
              <div className="rounded-xl border bg-[var(--card)] p-4 text-center">
                <div className="text-2xl font-bold text-emerald-400">-91%</div>
                <div className="text-[10px] text-[var(--muted-foreground)] mt-1">
                  Missed Edge Cases
                </div>
              </div>
            </div>
          </div>
        </ScrollReveal>

        {/* ── Section 3: How to Use ── */}
        <ScrollReveal>
          <div className="mb-6">
            <h2 className="text-2xl font-bold mb-2 text-center">How to Use</h2>
            <p className="text-sm text-[var(--muted-foreground)] text-center mb-10 max-w-xl mx-auto">
              Three steps from raw task to production-grade output.
            </p>
          </div>
        </ScrollReveal>

        <div className="space-y-4 mb-20">
          {usageSteps.map((step, i) => (
            <ScrollReveal key={step.num} delay={0.08 * i}>
              <div className="rounded-xl border bg-[var(--card)] p-5">
                <div className="flex items-start gap-4">
                  <span
                    className={`text-sm font-bold font-mono w-8 h-8 rounded-lg flex items-center justify-center shrink-0 ${step.bg} ${step.color}`}
                  >
                    {step.num}
                  </span>
                  <div>
                    <h3 className="text-base font-bold mb-1">{step.title}</h3>
                    <p className="text-sm text-[var(--muted-foreground)] leading-relaxed">
                      {step.desc}
                    </p>
                  </div>
                </div>
              </div>
            </ScrollReveal>
          ))}
        </div>

        {/* ── Section 4: Model-Specific Enhancement ── */}
        <ScrollReveal delay={0.1}>
          <div className="mb-20">
            <h2 className="text-2xl font-bold mb-2 text-center">Model-Specific Enhancement</h2>
            <p className="text-sm text-[var(--muted-foreground)] text-center mb-8 max-w-xl mx-auto">
              Each model family gets prompts structured for how it actually attends to instructions.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="rounded-xl border border-purple-500/20 bg-[var(--card)] p-5">
                <div className="text-sm font-bold text-purple-400 mb-3 font-mono">enhance-claude</div>
                <ul className="space-y-2">
                  {[
                    "XML tags for structure",
                    "Critical instructions at end (recency effect)",
                    "Few-shot examples with <example> tags",
                    "Explicit success criteria in <constraints>",
                  ].map((pt) => (
                    <li
                      key={pt}
                      className="flex items-start gap-2 text-xs text-[var(--muted-foreground)]"
                    >
                      <span className="text-purple-400 mt-0.5 shrink-0">▸</span>
                      {pt}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="rounded-xl border border-emerald-500/20 bg-[var(--card)] p-5">
                <div className="text-sm font-bold text-green-400 mb-3 font-mono">enhance-gpt</div>
                <ul className="space-y-2">
                  {[
                    "Markdown headers for structure",
                    "Critical instructions at start (primacy effect)",
                    "System-level context framing",
                    "Delimiters for code/data boundaries",
                  ].map((pt) => (
                    <li
                      key={pt}
                      className="flex items-start gap-2 text-xs text-[var(--muted-foreground)]"
                    >
                      <span className="text-green-400 mt-0.5 shrink-0">▸</span>
                      {pt}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </ScrollReveal>

        {/* ── Section 5: Example ── */}
        <ScrollReveal delay={0.15}>
          <div>
            <h2 className="text-2xl font-bold mb-2 text-center">Example Session</h2>
            <p className="text-sm text-[var(--muted-foreground)] text-center mb-6 max-w-xl mx-auto">
              The enhanced prompt is shown for review before execution.
            </p>
            <CodeEditor filename="cursor-chat">
              <pre className="text-[var(--foreground)] text-xs sm:text-sm leading-relaxed font-mono whitespace-pre">
                <code>{chatExample}</code>
              </pre>
            </CodeEditor>
          </div>
        </ScrollReveal>
      </div>
    </section>
  );
}
