import { FeatureCard } from "./FeatureCard";
import { ScrollReveal } from "./ScrollReveal";
import { CodeEditor } from "./CodeEditor";

const wakeCode = `# Option 1: Touch the wake file
touch ~/.cursor/skills/durable-request/.deep-sleep-wake

# Option 2: Kill the deep-sleep process
# Click terminal's stop button, or:
kill $(pgrep -f deep-sleep.sh)

# Agent immediately resumes with full context
# No extra request consumed`;

export function FeatureDeepSleep() {
  return (
    <div id="deep-sleep">
    <FeatureCard
      icon={
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
        </svg>
      }
      title="Sleep Without Losing Context"
      subtitle="Deep Sleep Recovery"
      description="Traditional prompt-based sleep (making AskQuestion wait) risks agent termination with no good wake mechanism — only fixed-time sleep is possible. Deep-sleep uses a real background Shell process that you can kill anytime to wake the agent, even after Cursor's timeout hides the AskQuestion UI."
      reversed
    >
      <div className="space-y-6">
        <ScrollReveal delay={0.2}>
          <div className="grid grid-cols-2 gap-3">
            <div className="rounded-xl border bg-[var(--card)] overflow-hidden">
              <div className="px-4 py-3 border-b bg-red-500/10 flex items-center gap-2">
                <div className="w-2.5 h-2.5 rounded-full bg-red-500 shrink-0" />
                <span className="text-xs font-medium text-[var(--foreground)]">Prompt-based sleep</span>
              </div>
              <div className="p-4">
                <ul className="text-xs text-[var(--muted-foreground)] space-y-1.5 list-disc list-inside">
                  <li>AskQuestion blocks → agent may terminate</li>
                  <li>Only fixed-time sleep possible</li>
                  <li>No wake mechanism</li>
                  <li>If UI times out → session lost</li>
                </ul>
              </div>
            </div>
            <div className="rounded-xl border bg-[var(--card)] overflow-hidden">
              <div className="px-4 py-3 border-b bg-emerald-500/10 flex items-center gap-2">
                <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 shrink-0" />
                <span className="text-xs font-medium text-[var(--foreground)] font-mono">deep-sleep.sh</span>
              </div>
              <div className="p-4">
                <ul className="text-xs text-[var(--muted-foreground)] space-y-1.5 list-disc list-inside">
                  <li>Real Shell process → killable anytime</li>
                  <li>Polls for wake file every 5s</li>
                  <li>Kill process or touch file to wake</li>
                  <li>Agent resumes with full context</li>
                </ul>
              </div>
            </div>
          </div>
        </ScrollReveal>

        <ScrollReveal delay={0.3}>
          <CodeEditor filename="wake-agent.sh">
            <pre className="text-[var(--foreground)] text-xs">
              <code>{wakeCode}</code>
            </pre>
          </CodeEditor>
        </ScrollReveal>

        <ScrollReveal delay={0.4}>
          <div className="grid grid-cols-2 gap-3">
            <div className="rounded-xl border bg-[var(--card)] p-4 text-center">
              <div className="text-3xl font-bold text-accent-500">2h</div>
              <div className="text-xs text-[var(--muted-foreground)] mt-1">Max sleep time</div>
            </div>
            <div className="rounded-xl border bg-[var(--card)] p-4 text-center">
              <div className="text-3xl font-bold text-accent-500">5s</div>
              <div className="text-xs text-[var(--muted-foreground)] mt-1">Wake response</div>
            </div>
          </div>
        </ScrollReveal>
      </div>
    </FeatureCard>
    </div>
  );
}
