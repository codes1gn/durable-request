import { FeatureCard } from "./FeatureCard";
import { ScrollReveal } from "./ScrollReveal";

const dimensions = [
  { label: "Structure", raw: 4.67, enhanced: 5.0 },
  { label: "Completeness", raw: 3.67, enhanced: 4.67 },
  { label: "Type Safety", raw: 4.67, enhanced: 5.0 },
  { label: "Error Handling", raw: 3.33, enhanced: 4.0 },
  { label: "Testability", raw: 4.0, enhanced: 5.0 },
];

const maxScore = 5;

export function FeatureEnhanceMe() {
  return (
    <div id="enhance-me">
    <FeatureCard
      icon={
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z" />
          <path d="M5 3v4" />
          <path d="M19 17v4" />
          <path d="M3 5h4" />
          <path d="M17 19h4" />
        </svg>
      }
      title="16.4% Better Code, Same Model"
      subtitle="/enhance-me Prompt Enhancer"
      description="Drop /enhance-me before any task. A subagent transforms your raw prompt using model-specific best practices — XML structuring for Claude, primacy-optimized headers for GPT. Same model, dramatically better output."
    >
      <div className="space-y-6">
        <ScrollReveal delay={0.2}>
          <div className="rounded-xl border bg-[var(--card)] overflow-hidden">
            <div className="px-4 py-3 border-b bg-[var(--muted)] text-xs font-medium text-[var(--muted-foreground)]">
              Code Quality Scores (1–5 scale, n=3 tasks)
            </div>
            <div className="p-5 space-y-4">
              {dimensions.map((dim) => (
                <div key={dim.label}>
                  <div className="text-xs text-[var(--muted-foreground)] mb-2">{dim.label}</div>
                  <div className="space-y-1.5">
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] w-14 shrink-0 text-[var(--muted-foreground)]">Raw</span>
                      <div className="flex-1 h-3 bg-[var(--muted)] rounded-full overflow-hidden">
                        <div
                          className="h-full bg-accent-500/40 rounded-full transition-all duration-1000"
                          style={{ width: `${(dim.raw / maxScore) * 100}%` }}
                        />
                      </div>
                      <span className="font-mono text-xs w-8 text-right text-[var(--foreground)]">
                        {dim.raw.toFixed(2)}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] w-14 shrink-0 text-[var(--muted-foreground)]">Enhanced</span>
                      <div className="flex-1 h-3 bg-[var(--muted)] rounded-full overflow-hidden">
                        <div
                          className="h-full bg-emerald-500 rounded-full transition-all duration-1000"
                          style={{ width: `${(dim.enhanced / maxScore) * 100}%` }}
                        />
                      </div>
                      <span className="font-mono text-xs w-8 text-right font-semibold text-emerald-500">
                        {dim.enhanced.toFixed(2)}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </ScrollReveal>

        <ScrollReveal delay={0.3}>
          <div className="grid grid-cols-3 gap-3">
            <div className="rounded-xl border bg-[var(--card)] p-4 text-center">
              <div className="text-2xl font-bold text-emerald-500">+16.4%</div>
              <div className="text-[10px] text-[var(--muted-foreground)] mt-1">Quality Gain</div>
            </div>
            <div className="rounded-xl border bg-[var(--card)] p-4 text-center">
              <div className="text-2xl font-bold text-emerald-500">+58%</div>
              <div className="text-[10px] text-[var(--muted-foreground)] mt-1">More Tests</div>
            </div>
            <div className="rounded-xl border bg-[var(--card)] p-4 text-center">
              <div className="text-2xl font-bold text-emerald-500">-91%</div>
              <div className="text-[10px] text-[var(--muted-foreground)] mt-1">Missed Edge Cases</div>
            </div>
          </div>
        </ScrollReveal>

        <ScrollReveal delay={0.4}>
          <div className="rounded-xl border bg-[var(--card)] overflow-hidden">
            <div className="px-4 py-3 border-b bg-[var(--muted)] text-xs font-medium text-[var(--muted-foreground)]">
              How it works
            </div>
            <div className="p-4 flex flex-wrap items-center justify-center gap-2 font-mono text-xs text-[var(--foreground)]">
              <span className="px-2 py-1 rounded bg-[var(--muted)]">/enhance-me task</span>
              <span className="text-[var(--muted-foreground)]">→</span>
              <span className="px-2 py-1 rounded bg-[var(--muted)]">subagent enhances</span>
              <span className="text-[var(--muted-foreground)]">→</span>
              <span className="px-2 py-1 rounded bg-[var(--muted)]">agent executes</span>
            </div>
          </div>
        </ScrollReveal>
      </div>
    </FeatureCard>
    </div>
  );
}
