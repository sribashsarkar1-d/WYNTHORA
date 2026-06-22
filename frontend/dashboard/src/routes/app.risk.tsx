import { createFileRoute } from "@tanstack/react-router";
import { Section, Badge } from "@/components/wynthora";

export const Route = createFileRoute("/app/risk")({ component: Risk });

const countries = [
  ["United States", 3.2, "success"], ["Germany", 4.1, "success"], ["China", 6.4, "warning"], ["Russia", 9.1, "danger"],
  ["Brazil", 5.8, "warning"], ["India", 5.2, "warning"], ["Japan", 3.0, "success"], ["Iran", 8.7, "danger"],
  ["Argentina", 7.9, "danger"], ["Turkey", 7.2, "danger"], ["South Africa", 6.6, "warning"], ["Saudi Arabia", 5.1, "warning"],
];

function Risk() {
  return (
    <div className="space-y-4">
      <div>
        <p className="text-xs uppercase tracking-widest text-muted-foreground">Composite scoring · 197 countries</p>
        <h1 className="font-display text-3xl font-bold">Global Risk Intelligence</h1>
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <Section title="Risk heatmap" className="lg:col-span-2">
          <div className="grid grid-cols-12 gap-1">
            {Array.from({ length: 96 }).map((_, i) => {
              const v = Math.random();
              const c = v < 0.3 ? "var(--color-success)" : v < 0.6 ? "var(--color-warning)" : "var(--color-destructive)";
              return <div key={i} className="aspect-square rounded-sm" style={{ background: c, opacity: 0.3 + v * 0.7 }} title={`risk ${(v * 10).toFixed(1)}`} />;
            })}
          </div>
          <div className="mt-3 flex justify-between text-[10px] text-muted-foreground"><span>Low risk</span><span>High risk</span></div>
        </Section>

        <Section title="Risk matrix (likelihood × impact)">
          <div className="relative aspect-square">
            <svg viewBox="0 0 200 200" className="h-full w-full">
              <rect x="0" y="0" width="200" height="200" fill="oklch(0.18 0.04 250)" />
              {[0, 1, 2, 3, 4].map((i) => (<g key={i}>
                <line x1={i * 50} y1="0" x2={i * 50} y2="200" stroke="oklch(1 0 0 / 0.1)" />
                <line x1="0" y1={i * 50} x2="200" y2={i * 50} stroke="oklch(1 0 0 / 0.1)" />
              </g>))}
              <rect x="100" y="0" width="100" height="100" fill="var(--color-destructive)" opacity="0.15" />
              <rect x="0" y="100" width="100" height="100" fill="var(--color-success)" opacity="0.15" />
              {[[40, 150, "cyan"], [130, 60, "destructive"], [80, 90, "warning"], [160, 30, "destructive"], [60, 120, "success"]].map(([x, y, c], i) => (
                <circle key={i} cx={x} cy={y} r="8" fill={`var(--color-${c})`} opacity="0.8" />
              ))}
              <text x="5" y="195" className="fill-muted-foreground text-[8px]">low impact</text>
              <text x="140" y="195" className="fill-muted-foreground text-[8px]">high impact</text>
            </svg>
          </div>
        </Section>
      </div>

      <Section title="Country risk rankings">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="text-xs uppercase tracking-wider text-muted-foreground">
              <tr className="border-b border-border"><th className="py-2 text-left">Rank</th><th className="text-left">Country</th><th>Composite</th><th>Economic</th><th>Political</th><th>Climate</th><th>Status</th></tr>
            </thead>
            <tbody>
              {countries.sort((a, b) => (b[1] as number) - (a[1] as number)).map(([c, v, t], i) => (
                <tr key={c as string} className="border-b border-border/50">
                  <td className="py-2.5 font-mono text-muted-foreground">{(i + 1).toString().padStart(2, "0")}</td>
                  <td className="font-medium">{c}</td>
                  <td className="text-center font-mono">{v}</td>
                  <td className="text-center text-muted-foreground">{((v as number) + Math.random() - 0.5).toFixed(1)}</td>
                  <td className="text-center text-muted-foreground">{((v as number) + Math.random() - 0.5).toFixed(1)}</td>
                  <td className="text-center text-muted-foreground">{((v as number) + Math.random() - 0.5).toFixed(1)}</td>
                  <td className="text-center"><Badge tone={t as any}>{t === "danger" ? "elevated" : t === "warning" ? "watch" : "stable"}</Badge></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Section>
    </div>
  );
}
