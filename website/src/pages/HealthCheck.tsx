import { motion } from "framer-motion";
import { ScrollReveal } from "../components/ScrollReveal";

// ── Static test data from testing/results/run-2026-04-15/analysis.json ──────
const RUN_DATE = "2026-04-15";
const TOTAL_SESSIONS = 10;
const MIN_REQUIRED_SAMPLES = 10; // for most features (F9 needs 5)

interface FeatureStat {
  id: string;
  name: string;
  passed: number;
  total: number;
  successRate: number;
  minRequired: number;
  group: "checkpoint" | "steering" | "loop" | "cleanup" | "platform";
}

const FEATURES: FeatureStat[] = [
  { id: "F1",  name: "Checkpoint after task completion",       passed: 8, total: 8,  successRate: 1.0, minRequired: 10, group: "checkpoint" },
  { id: "F2",  name: "TodoWrite + AskQuestion in same batch",  passed: 5, total: 5,  successRate: 1.0, minRequired: 10, group: "checkpoint" },
  { id: "F3",  name: "4 options (A/B/C context + D empty)",   passed: 4, total: 4,  successRate: 1.0, minRequired: 10, group: "checkpoint" },
  { id: "F4",  name: "Task summary in checkpoint prompt",      passed: 5, total: 5,  successRate: 1.0, minRequired: 10, group: "checkpoint" },
  { id: "F5",  name: "Multi-step checkpoint loop",             passed: 3, total: 3,  successRate: 1.0, minRequired: 10, group: "loop" },
  { id: "F6",  name: "Durable loop (continue until Done)",     passed: 3, total: 3,  successRate: 1.0, minRequired: 10, group: "loop" },
  { id: "F7",  name: "Subagent conversational fallback",       passed: 1, total: 1,  successRate: 1.0, minRequired: 10, group: "platform" },
  { id: "F8",  name: "Steering acknowledgment (header)",       passed: 1, total: 1,  successRate: 1.0, minRequired: 10, group: "steering" },
  { id: "F8a", name: "Steering visible in Shell output",       passed: 1, total: 1,  successRate: 1.0, minRequired: 10, group: "steering" },
  { id: "F8b", name: "Steering bounding box in reply",         passed: 1, total: 1,  successRate: 1.0, minRequired: 10, group: "steering" },
  { id: "F9",  name: "Todo cleanup at >20 items",              passed: 1, total: 1,  successRate: 1.0, minRequired: 5,  group: "cleanup" },
  { id: "F10", name: "No silent completion",                   passed: 6, total: 6,  successRate: 1.0, minRequired: 10, group: "checkpoint" },
];

interface WorkloadResult {
  id: string;
  label: string;
  passed: number;
  total: number;
  checkpointCount: number;
  features: string[];
}

const WORKLOADS: WorkloadResult[] = [
  { id: "01", label: "Simple Task",       passed: 5, total: 5, checkpointCount: 2,  features: ["F1","F2","F3","F4","F10"] },
  { id: "02", label: "Multi-Step",        passed: 7, total: 7, checkpointCount: 4,  features: ["F1","F2","F3","F4","F5","F6","F10"] },
  { id: "03", label: "Iterative",         passed: 3, total: 3, checkpointCount: 3,  features: ["F3","F5","F6"] },
  { id: "04", label: "Research",          passed: 4, total: 4, checkpointCount: 2,  features: ["F1","F2","F4","F10"] },
  { id: "05", label: "Debug",             passed: 4, total: 4, checkpointCount: 2,  features: ["F1","F2","F4","F10"] },
  { id: "06", label: "Steering",          passed: 4, total: 4, checkpointCount: 1,  features: ["F1","F8","F8a","F8b"] },
  { id: "07", label: "Long Task",         passed: 2, total: 2, checkpointCount: 6,  features: ["F1","F9"] },
  { id: "08", label: "Q&A",              passed: 2, total: 2, checkpointCount: 2,  features: ["F1","F10"] },
  { id: "09", label: "Subagent",          passed: 1, total: 1, checkpointCount: 2,  features: ["F7"] },
  { id: "10", label: "Composite",         passed: 7, total: 7, checkpointCount: 6,  features: ["F1","F2","F3","F4","F5","F6","F10"] },
];

const GROUP_META: Record<string, { label: string; color: string; border: string; bg: string }> = {
  checkpoint: { label: "Checkpoint",   color: "text-accent-400",   border: "border-accent-500/30",   bg: "bg-accent-500/10" },
  loop:       { label: "Durable Loop", color: "text-cyan-400",     border: "border-cyan-500/30",     bg: "bg-cyan-500/10" },
  steering:   { label: "Steering",     color: "text-amber-400",    border: "border-amber-500/30",    bg: "bg-amber-500/10" },
  cleanup:    { label: "Cleanup",      color: "text-violet-400",   border: "border-violet-500/30",   bg: "bg-violet-500/10" },
  platform:   { label: "Platform",     color: "text-emerald-400",  border: "border-emerald-500/30",  bg: "bg-emerald-500/10" },
};

const TOTAL_CHECKPOINTS = WORKLOADS.reduce((s, w) => s + w.checkpointCount, 0);
const ALL_PASS = FEATURES.every((f) => f.successRate === 1.0);

function ProgressBar({ value, max, color }: { value: number; max: number; color: string }) {
  const pct = max > 0 ? (value / max) * 100 : 0;
  return (
    <div className="h-1.5 w-full rounded-full bg-[var(--muted)] overflow-hidden">
      <motion.div
        className={`h-full rounded-full ${color}`}
        initial={{ width: 0 }}
        animate={{ width: `${pct}%` }}
        transition={{ duration: 0.6, ease: "easeOut" }}
      />
    </div>
  );
}

export function HealthCheck() {
  const groupedFeatures = Object.entries(GROUP_META).map(([key, meta]) => ({
    key,
    meta,
    features: FEATURES.filter((f) => f.group === key),
  }));

  return (
    <section className="relative min-h-screen">
      <div className="absolute inset-0 bg-grid opacity-40 dark:opacity-20" />
      <div className="absolute top-1/4 right-1/4 w-[500px] h-[500px] rounded-full bg-accent-400/8 dark:bg-accent-500/5 blur-3xl" />
      <div className="absolute bottom-1/3 left-1/4 w-[400px] h-[400px] rounded-full bg-cyan-400/8 dark:bg-cyan-500/5 blur-3xl" />

      <div className="relative max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-24 pb-20">

        {/* ── Header ── */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="mb-16 text-center"
        >
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border bg-[var(--card)] text-sm mb-6">
            <span className={`w-2 h-2 rounded-full ${ALL_PASS ? "bg-emerald-400 animate-pulse" : "bg-rose-400"}`} />
            <span className="text-[var(--muted-foreground)] font-mono text-xs">
              run-{RUN_DATE}
            </span>
          </div>
          <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight mb-4">
            Health Check
          </h1>
          <p className="text-lg text-[var(--muted-foreground)] max-w-2xl mx-auto">
            Systematic test results across all durable-request features.
            Each workload session is analyzed for protocol compliance via pattern matching on transcripts.
          </p>
        </motion.div>

        {/* ── Top-level KPIs ── */}
        <ScrollReveal>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-14">
            {[
              { label: "Workloads",       value: `${TOTAL_SESSIONS}/10`,    sub: "all passed",          color: "text-emerald-400" },
              { label: "Features",        value: `${FEATURES.length}`,      sub: "verified",            color: "text-accent-400" },
              { label: "Pass Rate",       value: "100%",                    sub: "on all samples",      color: "text-emerald-400" },
              { label: "Checkpoints",     value: `${TOTAL_CHECKPOINTS}`,    sub: "total in baseline",   color: "text-cyan-400" },
            ].map((kpi) => (
              <div key={kpi.label} className="rounded-xl border bg-[var(--card)] p-5 text-center">
                <div className={`text-3xl font-extrabold ${kpi.color} mb-1`}>{kpi.value}</div>
                <div className="text-xs font-semibold mb-0.5">{kpi.label}</div>
                <div className="text-xs text-[var(--muted-foreground)]">{kpi.sub}</div>
              </div>
            ))}
          </div>
        </ScrollReveal>

        {/* ── Feature Results by Group ── */}
        <ScrollReveal>
          <h2 className="text-xl font-bold mb-6">Feature Results</h2>
        </ScrollReveal>

        <div className="space-y-6 mb-14">
          {groupedFeatures.map(({ key, meta, features }) => (
            <ScrollReveal key={key} delay={0.05}>
              <div className={`rounded-xl border ${meta.border} bg-[var(--card)] overflow-hidden`}>
                <div className={`px-5 py-3 border-b ${meta.border} ${meta.bg}`}>
                  <span className={`text-xs font-bold uppercase tracking-wider ${meta.color}`}>
                    {meta.label}
                  </span>
                </div>
                <div className="divide-y divide-[var(--border)]">
                  {features.map((f) => {
                    const samplePct = Math.min(f.total / f.minRequired, 1) * 100;
                    const isLowSample = f.total < f.minRequired;
                    return (
                      <div key={f.id} className="px-5 py-4">
                        <div className="flex items-center justify-between mb-1.5">
                          <div className="flex items-center gap-2.5">
                            <span className={`text-xs font-mono font-bold ${meta.color}`}>{f.id}</span>
                            <span className="text-sm">{f.name}</span>
                          </div>
                          <div className="flex items-center gap-3 shrink-0 ml-4">
                            <span className="text-xs text-[var(--muted-foreground)] font-mono">
                              {f.passed}/{f.total}
                            </span>
                            <span className="text-xs font-bold text-emerald-400">
                              {Math.round(f.successRate * 100)}%
                            </span>
                            {isLowSample ? (
                              <span className="text-[10px] px-1.5 py-0.5 rounded bg-[var(--muted)] text-[var(--muted-foreground)] font-mono whitespace-nowrap">
                                need {f.minRequired - f.total} more
                              </span>
                            ) : (
                              <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/15 text-emerald-400 font-mono">
                                certified
                              </span>
                            )}
                          </div>
                        </div>
                        {/* Two progress bars: pass rate + sample coverage */}
                        <div className="space-y-1">
                          <ProgressBar value={f.passed} max={f.total} color="bg-emerald-400" />
                          <div className="flex justify-between items-center">
                            <span className="text-[10px] text-[var(--muted-foreground)]">
                              sample coverage {f.total}/{f.minRequired} (min {f.minRequired})
                            </span>
                          </div>
                          <ProgressBar value={f.total} max={f.minRequired} color={samplePct >= 1 ? "bg-emerald-400" : "bg-amber-400"} />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </ScrollReveal>
          ))}
        </div>

        {/* ── Workload Matrix ── */}
        <ScrollReveal>
          <h2 className="text-xl font-bold mb-4">Workload Coverage Matrix</h2>
          <p className="text-sm text-[var(--muted-foreground)] mb-6">
            Each row is one workload session. Columns show which features were verified. All 10 sessions passed.
          </p>
          <div className="rounded-xl border bg-[var(--card)] overflow-hidden mb-14">
            {/* Header row */}
            <div className="overflow-x-auto">
              <table className="w-full text-xs">
                <thead>
                  <tr className="border-b bg-[var(--muted)]/40">
                    <th className="text-left px-4 py-2.5 font-semibold text-[var(--muted-foreground)] whitespace-nowrap">
                      Workload
                    </th>
                    <th className="px-2 py-2.5 font-semibold text-[var(--muted-foreground)] text-center">Ckpts</th>
                    {FEATURES.map((f) => (
                      <th key={f.id} className="px-2 py-2.5 font-mono text-center text-[var(--muted-foreground)]">
                        {f.id}
                      </th>
                    ))}
                    <th className="px-4 py-2.5 font-semibold text-[var(--muted-foreground)] text-center whitespace-nowrap">
                      Result
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {WORKLOADS.map((w, i) => (
                    <tr key={w.id} className={i !== WORKLOADS.length - 1 ? "border-b border-[var(--border)]" : ""}>
                      <td className="px-4 py-2.5 whitespace-nowrap">
                        <span className="font-mono text-[var(--muted-foreground)] mr-2">{w.id}</span>
                        <span className="font-medium">{w.label}</span>
                      </td>
                      <td className="px-2 py-2.5 text-center font-mono text-[var(--muted-foreground)]">
                        {w.checkpointCount}
                      </td>
                      {FEATURES.map((f) => {
                        const hit = w.features.includes(f.id);
                        return (
                          <td key={f.id} className="px-2 py-2.5 text-center">
                            {hit ? (
                              <span className="text-emerald-400 font-bold">✓</span>
                            ) : (
                              <span className="text-[var(--border)]">·</span>
                            )}
                          </td>
                        );
                      })}
                      <td className="px-4 py-2.5 text-center">
                        <span className="text-emerald-400 font-bold text-xs">
                          {w.passed}/{w.total}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
                {/* Feature totals row */}
                <tfoot>
                  <tr className="border-t bg-[var(--muted)]/40">
                    <td className="px-4 py-2.5 font-semibold text-xs text-[var(--muted-foreground)]">
                      Sessions
                    </td>
                    <td className="px-2 py-2.5 text-center font-mono font-bold text-[var(--foreground)]">
                      {TOTAL_CHECKPOINTS}
                    </td>
                    {FEATURES.map((f) => {
                      const count = WORKLOADS.filter((w) => w.features.includes(f.id)).length;
                      return (
                        <td key={f.id} className="px-2 py-2.5 text-center font-mono font-bold text-[var(--foreground)]">
                          {count}
                        </td>
                      );
                    })}
                    <td className="px-4 py-2.5 text-center font-bold text-emerald-400">
                      10/10
                    </td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </div>
        </ScrollReveal>

        {/* ── Sample Coverage Notice ── */}
        <ScrollReveal>
          <div className="rounded-xl border border-amber-500/25 bg-amber-500/5 p-5 mb-14">
            <div className="flex items-start gap-3">
              <span className="text-amber-400 text-lg shrink-0">⚠</span>
              <div>
                <div className="text-sm font-bold text-amber-400 mb-1">Baseline run — single sample per workload</div>
                <p className="text-xs text-[var(--muted-foreground)] leading-relaxed">
                  This baseline run has 1 session per workload (10 total). Full certification requires {MIN_REQUIRED_SAMPLES} sessions per
                  workload for most features (5 for F9). Pass rate is 100% across all samples.
                  To collect full samples: <code className="px-1 py-0.5 rounded bg-[var(--muted)] font-mono">./testing/scripts/run-all.sh --runs 10</code>
                </p>
              </div>
            </div>
          </div>
        </ScrollReveal>

        {/* ── Testing Architecture ── */}
        <ScrollReveal>
          <h2 className="text-xl font-bold mb-4">Testing Architecture</h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
            {[
              {
                icon: "📄",
                title: "Workload definitions",
                desc: "10 .md files in testing/workloads/ — each defines a prompt, expected behavior, and features to verify",
                mono: "testing/workloads/NN-*.md",
              },
              {
                icon: "📑",
                title: "Session transcripts",
                desc: "Plain-text captures of agent sessions — tool calls, responses, checkpoints, and steering events",
                mono: "testing/results/run-DATE/*.txt",
              },
              {
                icon: "🔍",
                title: "Pattern matching",
                desc: "Python regex patterns for each feature. analyze.py runs against all transcripts and reports pass/fail",
                mono: "testing/scripts/analyze.py",
              },
            ].map((card) => (
              <div key={card.title} className="rounded-xl border bg-[var(--card)] p-5">
                <div className="text-2xl mb-2">{card.icon}</div>
                <div className="text-sm font-bold mb-1">{card.title}</div>
                <p className="text-xs text-[var(--muted-foreground)] leading-relaxed mb-2">{card.desc}</p>
                <code className="text-[10px] font-mono text-accent-400 bg-accent-500/10 px-1.5 py-0.5 rounded">
                  {card.mono}
                </code>
              </div>
            ))}
          </div>
        </ScrollReveal>

        {/* ── Feature Legend ── */}
        <ScrollReveal delay={0.1}>
          <div className="rounded-xl border bg-[var(--card)] p-5">
            <h3 className="text-sm font-bold mb-4 text-[var(--muted-foreground)] uppercase tracking-wider">
              Feature Legend
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-2">
              {FEATURES.map((f) => {
                const meta = GROUP_META[f.group];
                return (
                  <div key={f.id} className="flex items-center gap-3">
                    <span className={`text-xs font-mono font-bold shrink-0 w-8 ${meta.color}`}>
                      {f.id}
                    </span>
                    <span className="text-xs text-[var(--muted-foreground)]">{f.name}</span>
                  </div>
                );
              })}
            </div>
          </div>
        </ScrollReveal>

      </div>
    </section>
  );
}
