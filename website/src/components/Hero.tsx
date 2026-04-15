import { motion } from "framer-motion";
import { CodeEditor } from "./CodeEditor";
import mascotLogo from "../assets/durable-request-mascot-logo.png";
import exampleSessionRaw from "../assets/durable-request-example.md?raw";

function ValuePillar({
  icon,
  badge,
  title,
  points,
  metrics,
  variant,
}: {
  icon: React.ReactNode;
  badge: string;
  title: string;
  points: { strong: string; rest: string }[];
  metrics: { value: string; label: string }[];
  variant: "blue" | "green";
}) {
  const s = variant === "blue"
    ? {
        border: "border-accent-500/20 hover:border-accent-500/40",
        glow: "bg-accent-500/5 group-hover:bg-accent-500/15",
        badge: "bg-accent-500/15 text-accent-400",
        dot: "bg-accent-500",
        metric: "text-accent-400",
        ring: "ring-accent-500/20",
        gradient: "from-accent-500/10 via-transparent to-transparent",
      }
    : {
        border: "border-emerald-500/20 hover:border-emerald-500/40",
        glow: "bg-emerald-500/5 group-hover:bg-emerald-500/15",
        badge: "bg-emerald-500/15 text-emerald-400",
        dot: "bg-emerald-500",
        metric: "text-emerald-400",
        ring: "ring-emerald-500/20",
        gradient: "from-emerald-500/10 via-transparent to-transparent",
      };

  return (
    <div
      className={`relative rounded-2xl ${s.border} border bg-[var(--card)] overflow-hidden group transition-all duration-300 hover:shadow-xl hover:shadow-black/10`}
    >
      <div className={`absolute inset-0 bg-gradient-to-br ${s.gradient} opacity-50`} />
      <div
        className={`absolute top-0 right-0 w-72 h-72 rounded-full ${s.glow} blur-3xl -translate-y-1/2 translate-x-1/3 transition-all duration-500`}
      />

      <div className="relative p-8">
        <div
          className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full ${s.badge} text-xs font-semibold mb-5 uppercase tracking-wider`}
        >
          {icon}
          {badge}
        </div>

        <h3 className="text-2xl sm:text-3xl font-extrabold tracking-tight mb-6">
          {title}
        </h3>

        <div className="space-y-3 mb-8">
          {points.map((pt, j) => (
            <div key={j} className="flex items-start gap-3">
              <div className={`mt-1.5 w-2 h-2 rounded-full ${s.dot} shrink-0`} />
              <p className="text-[var(--muted-foreground)] text-sm leading-relaxed">
                <span className="text-[var(--foreground)] font-semibold">
                  {pt.strong}
                </span>
                {pt.rest}
              </p>
            </div>
          ))}
        </div>

        <div className={`grid grid-cols-${metrics.length} gap-3 pt-6 border-t border-[var(--border)]`}>
          {metrics.map((m) => (
            <div key={m.label} className="text-center">
              <div className={`text-3xl font-extrabold ${s.metric}`}>
                {m.value}
              </div>
              <div className="text-xs text-[var(--muted-foreground)] mt-1">
                {m.label}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export function Hero() {
  return (
    <section className="relative overflow-hidden">
      <div className="absolute inset-0 bg-grid opacity-40 dark:opacity-20" />
      <div className="absolute top-1/3 left-1/4 w-[600px] h-[600px] rounded-full bg-accent-400/8 dark:bg-accent-500/5 blur-3xl" />
      <div className="absolute top-1/2 right-1/4 w-[500px] h-[500px] rounded-full bg-emerald-400/8 dark:bg-emerald-500/5 blur-3xl" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-20 sm:pt-32 sm:pb-28">
        <div className="flex flex-col items-center text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mb-4"
          >
            <img src={mascotLogo} alt="DurableRequest mascot" className="w-24 h-24 sm:w-28 sm:h-28" />
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.05 }}
            className="text-5xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight mb-3 text-gradient"
          >
            DurableRequest
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border bg-[var(--card)] text-sm mb-8"
          >
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-[var(--muted-foreground)]">
              One install — agent skill + steering hooks + IDE extension
            </span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.15 }}
            className="text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight max-w-4xl leading-[1.1] text-[var(--muted-foreground)]"
          >
            Work, checkpoint, respond, repeat —{" "}
            <span className="text-gradient font-extrabold text-[var(--foreground)]">all in one request.</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="mt-6 text-lg sm:text-xl text-[var(--muted-foreground)] max-w-3xl leading-relaxed"
          >
            A skill package that transforms AI agents from one-shot tools into
            interactive partners. Structured checkpoints, mid-task steering, and
            context that never resets — across Cursor, Claude Code, and Codex.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="mt-10 flex flex-col sm:flex-row gap-4"
          >
            <a
              href="#install"
              className="px-8 py-3.5 text-sm font-semibold bg-accent-500 text-white rounded-xl
                         hover:bg-accent-600 transition-all shadow-lg shadow-accent-500/25
                         hover:shadow-accent-500/40"
            >
              Install durable-request
            </a>
            <a
              href="#features"
              className="px-8 py-3.5 text-sm font-semibold border rounded-xl
                         hover:bg-[var(--muted)] transition-all"
            >
              See How It Works
            </a>
          </motion.div>
        </div>

        {/* Two Value Pillars */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.4 }}
          className="mt-20 grid grid-cols-1 lg:grid-cols-2 gap-6"
        >
          <ValuePillar
            variant="blue"
            icon={
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="22 7 13.5 15.5 8.5 10.5 2 17" />
                <polyline points="16 7 22 7 22 13" />
              </svg>
            }
            badge="For Teams & Managers"
            title="Maximize Cursor Team Plan ROI"
            points={[
              { strong: "Dev at full pace", rest: " — agents work continuously, not one-shot-and-gone" },
              { strong: "Longer sessions", rest: " — 5× to 10× more productive cycles per request" },
              { strong: "Zero wasted context", rest: " — no re-prompting, no lost state between requests" },
              { strong: "Compound productivity", rest: " — each loop iteration builds on everything before" },
            ]}
            metrics={[
              { value: "5×", label: "Session duration" },
              { value: "10×", label: "Peak output" },
              { value: "0", label: "Idle turns" },
            ]}
          />
          <ValuePillar
            variant="green"
            icon={
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5" />
                <path d="M9 18h6" />
                <path d="M10 22h4" />
              </svg>
            }
            badge="For Developers"
            title="Reveal the Agent's Black Box"
            points={[
              { strong: "Fine-grained control", rest: " — steer the agent at every checkpoint, not just at the start" },
              { strong: "More discussion", rest: " — align on approach before the agent writes 200 wrong lines" },
              { strong: "More feedback loops", rest: " — knowledge aligns incrementally, not retroactively" },
              { strong: "True peer-coding experience", rest: " — a real back-and-forth, not a monologue" },
            ]}
            metrics={[
              { value: "∞", label: "Checkpoints" },
              { value: "100%", label: "Adherence" },
              { value: "0", label: "Silent ends" },
            ]}
          />
        </motion.div>

        {/* Real Session Transcript */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.8 }}
          className="mt-16 w-full max-w-4xl mx-auto"
        >
          <h2 className="text-xl font-bold mb-2 text-center">
            Real Session — 6 Checkpoints, 1 Request
          </h2>
          <p className="text-sm text-[var(--muted-foreground)] text-center mb-4 max-w-2xl mx-auto">
            An actual Cursor CLI session where the agent writes a LinkedIn post,
            then iterates through 6 checkpoint loops — shortening, reframing, adjusting tone —
            all in a single request with full context.
          </p>
          <CodeEditor filename="cursor-agent session — exported from real run (df24bb15)">
            <pre className="text-[var(--foreground)] text-xs sm:text-sm max-h-[500px] overflow-y-auto leading-relaxed">
              <code>{exampleSessionRaw}</code>
            </pre>
          </CodeEditor>
        </motion.div>
      </div>
    </section>
  );
}
