import { createFileRoute } from "@tanstack/react-router";
import { Section, StatCard, Spark, Badge } from "@/components/wynthora";

export const Route = createFileRoute("/app/results")({ component: Results });

const s = (n: number) => Array.from({ length: 36 }, (_, i) => 50 + Math.sin(i / 3 + n) * 25 + (i * (n % 3 === 0 ? -0.5 : 0.8)));

function Results() {
  return (
    <div className="space-y-4">
      <div>
        <p className="text-xs uppercase tracking-widest text-muted-foreground">Sim #WYN-A14 · completed</p>
        <h1 className="font-display text-3xl font-bold">Prediction Results</h1>
      </div>

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <StatCard label="Confidence score" value="87.4%" delta="+2.1" data={s(1)} />
        <StatCard label="Convergence" value="0.94" data={s(2)} color="var(--color-success)" />
        <StatCard label="Mean GDP impact" value="-0.62%" delta="-0.18" data={s(3)} color="var(--color-warning)" />
        <StatCard label="Tail risk (P95)" value="-2.4%" data={s(4)} color="var(--color-purple)" />
      </div>

      <Section title="Forecast — German GDP, 2025–2030">
        <div className="relative h-64">
          <svg viewBox="0 0 600 240" className="h-full w-full">
            <defs><linearGradient id="band" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="oklch(0.78 0.18 220)" stopOpacity="0.3" /><stop offset="100%" stopColor="oklch(0.78 0.18 220)" stopOpacity="0" /></linearGradient></defs>
            {Array.from({ length: 5 }).map((_, i) => <line key={i} x1="0" y1={i * 50 + 20} x2="600" y2={i * 50 + 20} stroke="oklch(1 0 0 / 0.05)" />)}
            <path d="M0 140 Q 80 130 160 120 T 320 105 T 480 95 T 600 80" fill="none" stroke="var(--color-cyan)" strokeWidth="2" />
            <path d="M0 140 Q 80 110 160 90 T 320 70 T 480 55 T 600 40 L 600 130 Q 480 130 320 145 T 160 160 T 0 170 Z" fill="url(#band)" />
            <path d="M0 140 Q 80 160 160 175 T 320 195 T 480 210 T 600 220" fill="none" stroke="oklch(0.55 0.25 295)" strokeWidth="1" strokeDasharray="4 4" />
            {Array.from({ length: 6 }).map((_, i) => <text key={i} x={i * 100 + 10} y="235" className="fill-muted-foreground text-[10px]">{2025 + i}</text>)}
          </svg>
        </div>
        <div className="mt-3 flex gap-4 text-xs">
          <span className="flex items-center gap-1.5"><span className="h-2 w-4 rounded bg-cyan" /> P50 forecast</span>
          <span className="flex items-center gap-1.5"><span className="h-2 w-4 rounded bg-cyan/30" /> 95% confidence band</span>
          <span className="flex items-center gap-1.5"><span className="h-2 w-4 rounded bg-purple/50" /> Stress scenario</span>
        </div>
      </Section>

      <div className="grid gap-4 lg:grid-cols-2">
        <Section title="Probability distribution">
          <svg viewBox="0 0 400 180" className="w-full">
            {Array.from({ length: 40 }, (_, i) => {
              const h = Math.exp(-Math.pow((i - 20) / 6, 2)) * 140;
              return <rect key={i} x={i * 10} y={170 - h} width="8" height={h} fill="var(--color-cyan)" opacity={0.4 + Math.exp(-Math.pow((i - 20) / 6, 2)) * 0.6} />;
            })}
            <line x1="200" y1="20" x2="200" y2="170" stroke="var(--color-purple)" strokeDasharray="3 3" />
            <text x="205" y="30" className="fill-purple text-[10px]">P50: -0.62%</text>
          </svg>
        </Section>
        <Section title="Future outcomes (top 5)">
          <ul className="space-y-2 text-sm">
            {[
              ["Soft landing, WTO arbitration succeeds", 31, "success"],
              ["Tit-for-tat escalation, modest contraction", 28, "warning"],
              ["Full trade war, recession in EU manufacturing", 22, "danger"],
              ["Bilateral carve-out, neutral impact", 12, "cyan"],
              ["Black swan: third-party intervention", 7, "purple"],
            ].map(([t, p, tone]) => (
              <li key={t as string} className="glass rounded-lg p-3">
                <div className="flex items-center justify-between"><span>{t}</span><Badge tone={tone as any}>{p}%</Badge></div>
                <div className="mt-2 h-1 rounded-full bg-muted overflow-hidden"><div className="h-full rounded-full bg-gradient-to-r from-cyan to-purple" style={{ width: `${p}%` }} /></div>
              </li>
            ))}
          </ul>
        </Section>
      </div>
    </div>
  );
}
