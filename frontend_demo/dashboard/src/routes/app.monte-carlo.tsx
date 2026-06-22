import { createFileRoute } from "@tanstack/react-router";
import { Section, StatCard } from "@/components/wynthora";

export const Route = createFileRoute("/app/monte-carlo")({ component: MC });

const s = (n: number) => Array.from({ length: 30 }, (_, i) => 50 + Math.sin(i / 2 + n) * 20);

function MC() {
  return (
    <div className="space-y-4">
      <div>
        <p className="text-xs uppercase tracking-widest text-muted-foreground">Stochastic engine</p>
        <h1 className="font-display text-3xl font-bold">Monte Carlo Dashboard</h1>
      </div>
      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <StatCard label="Iterations" value="1,000,000" data={s(1)} />
        <StatCard label="Convergence" value="0.997" data={s(2)} color="var(--color-success)" />
        <StatCard label="CI width 95%" value="±1.8%" data={s(3)} color="var(--color-purple)" />
        <StatCard label="Outliers" value="0.04%" data={s(4)} color="var(--color-warning)" />
      </div>

      <Section title="Distribution of outcomes">
        <svg viewBox="0 0 800 240" className="w-full">
          {Array.from({ length: 60 }, (_, i) => {
            const h = Math.exp(-Math.pow((i - 30) / 9, 2)) * 200 + Math.random() * 10;
            return <rect key={i} x={i * 13} y={220 - h} width="11" height={h} fill="var(--color-cyan)" opacity={0.3 + Math.exp(-Math.pow((i - 30) / 9, 2)) * 0.7} />;
          })}
          <line x1="265" y1="20" x2="265" y2="220" stroke="var(--color-success)" strokeDasharray="3 3" />
          <line x1="515" y1="20" x2="515" y2="220" stroke="var(--color-warning)" strokeDasharray="3 3" />
          <text x="270" y="35" className="fill-success text-[10px]">P5: -2.4%</text>
          <text x="520" y="35" className="fill-warning text-[10px]">P95: +1.2%</text>
        </svg>
      </Section>

      <div className="grid gap-4 lg:grid-cols-2">
        <Section title="Iteration convergence">
          <svg viewBox="0 0 400 180" className="w-full">
            <path d="M0 100 Q 100 60 200 70 T 400 65" fill="none" stroke="var(--color-cyan)" strokeWidth="2" />
            <path d="M0 100 Q 100 130 200 110 T 400 95" fill="none" stroke="var(--color-purple)" strokeWidth="2" opacity="0.7" />
            <path d="M0 100 Q 100 90 200 88 T 400 80" fill="none" stroke="var(--color-success)" strokeWidth="2" opacity="0.7" />
          </svg>
          <div className="mt-2 flex gap-4 text-xs"><span className="text-cyan">Scenario A</span><span className="text-purple">Scenario B</span><span className="text-success">Scenario C</span></div>
        </Section>
        <Section title="Scenario comparison">
          <table className="w-full text-sm">
            <thead className="text-xs text-muted-foreground"><tr><th className="text-left">Scenario</th><th>Mean</th><th>P5</th><th>P95</th><th>P(loss)</th></tr></thead>
            <tbody>
              {[["Baseline", "+0.4%", "-1.8%", "+2.4%", "31%"], ["Trade war", "-0.9%", "-3.7%", "+0.8%", "78%"], ["Soft landing", "+1.2%", "-0.4%", "+2.9%", "12%"], ["Black swan", "-2.4%", "-7.1%", "-0.2%", "94%"]].map(([n, ...vals]) => (
                <tr key={n} className="border-b border-border/50"><td className="py-2.5 font-medium">{n}</td>{vals.map((v, i) => <td key={i} className="text-center font-mono">{v}</td>)}</tr>
              ))}
            </tbody>
          </table>
        </Section>
      </div>
    </div>
  );
}
