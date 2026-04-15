import { motion } from "framer-motion";
import { ScrollReveal } from "../components/ScrollReveal";

interface ChangeEntry {
  type: "added" | "changed" | "fixed" | "note" | "test";
  text: string;
}

interface Release {
  version: string;
  date: string;
  highlight?: string;
  entries: ChangeEntry[];
}

const releases: Release[] = [
  {
    version: "1.2.0",
    date: "2026-04-15",
    highlight: "In-Continuation Steering — Redirect the Agent, Free of Request",
    entries: [
      { type: "added", text: "In-continuation steering: redirect the agent mid-task without interrupting or consuming an extra request — the hook injects your message at the next Shell call inside the same conversation" },
      { type: "added", text: "Mandatory STEERING RECEIVED bounding box: agent must echo message verbatim + adjusted plan in a visible box at the top of its reply" },
      { type: "added", text: "F8b test feature: pattern matcher verifies the full bounding box structure (⚡ STEERING RECEIVED header + Message row + Response row)" },
      { type: "added", text: "Test runner scripts: run-workload.sh and run-all.sh for end-to-end session automation with --filter, --runs, --dry-run, --analyze-only modes" },
      { type: "added", text: "First full baseline test run: testing/results/run-2026-04-15/ — 10/10 workloads pass, 12/12 features at 100% on first sample" },
      { type: "changed", text: "Stationary status bar: yellow Steering pending badge stays solid until file is consumed by hook, then clears within 1 second via adaptive polling (1 s pending / 5 s idle)" },
      { type: "changed", text: "Status bar label now shows the queued message: ⚡ Steering pending — \"focus on the API layer\"" },
      { type: "fixed", text: "Status bar flickered back to normal after 30 s even if message was not consumed — removed the 30-second timeout, replaced with file-based polling" },
      { type: "fixed", text: "Extension deactivation now properly clears the poll interval without leaking timers" },
      { type: "note", text: "Market gap: Claude Code, Codex, and Copilot IDE all had native steering; Cursor had none. durable-request v1.2 solves this for Cursor CLI via Shell command injection (preToolUse updated_input). Cursor IDE still unsupported." },
    ],
  },
  {
    version: "1.1.0",
    date: "2026-04-12",
    highlight: "Cursor CLI Checkpoint — True Durable Loop in Terminal",
    entries: [
      { type: "added", text: "Cursor CLI checkpoint (checkpoint.sh + checkpoint-ui.sh) — true blocking interactive checkpoints via tmux split panes, same durable loop as AskQuestion in the editor" },
      { type: "added", text: "Three-layer checkpoint architecture: AskQuestion (editor) → checkpoint.sh (CLI) → conversational fallback (subagents)" },
      { type: "test", text: "20-checkpoint continuation batch: 60/60 passed (20×continue, 20×iterate, 20×done = 100%)" },
      { type: "test", text: "Fresh install verification: SKILL.md + checkpoint scripts validated end-to-end" },
      { type: "test", text: "Graceful fallback without tmux confirmed (exit 0, explicit messaging)" },
    ],
  },
  {
    version: "1.0.1",
    date: "2026-04-11",
    entries: [
      { type: "added", text: "Epoch 3 A/B experiments (30 control + 30 treatment subagents)" },
      { type: "added", text: "Product website with animated feature demos" },
      { type: "added", text: "LAN serving script (serve.sh) + systemd service file" },
    ],
  },
  {
    version: "1.0.0",
    date: "2026-04-10",
    highlight: "Initial Release",
    entries: [
      { type: "added", text: "durable-request skill — universal end-of-task continuation gate" },
      { type: "added", text: "AskQuestion integration for Cursor editor" },
      { type: "added", text: "AskUserQuestion integration for Claude Code" },
      { type: "added", text: "question tool integration for OpenCode" },
      { type: "added", text: "Conversational fallback for all platforms" },
      { type: "added", text: "TodoWrite + AskQuestion reinforcement pattern (double-lock)" },
      { type: "added", text: "A/B experiment harness with 170 total subagent experiments across 3 epochs" },
    ],
  },
];

const typeBadge: Record<ChangeEntry["type"], { label: string; className: string }> = {
  added:   { label: "Added",   className: "bg-emerald-500/15 text-emerald-400" },
  changed: { label: "Changed", className: "bg-amber-500/15 text-amber-400" },
  fixed:   { label: "Fixed",   className: "bg-rose-500/15 text-rose-400" },
  note:    { label: "Note",    className: "bg-sky-500/15 text-sky-400" },
  test:    { label: "Test",    className: "bg-violet-500/15 text-violet-400" },
};

export function Changelog() {
  return (
    <section className="relative min-h-screen">
      <div className="absolute inset-0 bg-grid opacity-40 dark:opacity-20" />
      <div className="absolute top-1/4 left-1/3 w-[500px] h-[500px] rounded-full bg-accent-400/8 dark:bg-accent-500/5 blur-3xl" />

      <div className="relative max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-12"
        >
          <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight mb-4">
            Changelog
          </h1>
          <p className="text-lg text-[var(--muted-foreground)]">
            All notable changes to durable-request, documented with care.
          </p>
        </motion.div>

        <div className="space-y-12">
          {releases.map((release, ri) => (
            <ScrollReveal key={release.version} delay={0.1 * ri}>
              <article className="relative">
                <div className="flex items-center gap-4 mb-4">
                  <span className="text-2xl font-extrabold tracking-tight">
                    v{release.version}
                  </span>
                  <span className="text-sm text-[var(--muted-foreground)] px-3 py-1 rounded-full bg-[var(--muted)]">
                    {release.date}
                  </span>
                  {ri === 0 && (
                    <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-500/15 text-emerald-400 uppercase tracking-wider">
                      Latest
                    </span>
                  )}
                </div>

                {release.highlight && (
                  <p className="text-base font-semibold text-[var(--foreground)] mb-4 pl-1">
                    {release.highlight}
                  </p>
                )}

                <div className="rounded-xl border bg-[var(--card)] overflow-hidden">
                  {release.entries.map((entry, ei) => {
                    const badge = typeBadge[entry.type];
                    return (
                      <div
                        key={ei}
                        className={`flex items-start gap-3 px-5 py-3 ${
                          ei !== release.entries.length - 1 ? "border-b border-[var(--border)]" : ""
                        }`}
                      >
                        <span
                          className={`text-[10px] font-semibold px-2 py-0.5 rounded-full shrink-0 mt-0.5 uppercase tracking-wider ${badge.className}`}
                        >
                          {badge.label}
                        </span>
                        <span className="text-sm text-[var(--muted-foreground)] leading-relaxed">
                          {entry.text}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </article>
            </ScrollReveal>
          ))}
        </div>
      </div>
    </section>
  );
}
