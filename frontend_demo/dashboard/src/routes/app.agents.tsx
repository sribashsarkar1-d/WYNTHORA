import { createFileRoute } from "@tanstack/react-router";
import { Section, Badge } from "@/components/wynthora";

export const Route = createFileRoute("/app/agents")({ component: Agents });

const agents = [
  { n: "Macro-7", d: "Economy", s: "active", l: 94 },
  { n: "Geo-3", d: "Politics", s: "active", l: 87 },
  { n: "Climate-12", d: "Climate", s: "active", l: 91 },
  { n: "FX-2", d: "Markets", s: "active", l: 82 },
  { n: "Energy-1", d: "Commodities", s: "idle", l: 76 },
  { n: "Trade-5", d: "Supply chain", s: "active", l: 88 },
  { n: "Cyber-9", d: "Security", s: "active", l: 70 },
  { n: "Bio-4", d: "Pandemics", s: "idle", l: 65 },
];

function Agents() {
  return (
    <div className="space-y-4">
      <div>
        <p className="text-xs uppercase tracking-widest text-muted-foreground">42 specialist agents</p>
        <h1 className="font-display text-3xl font-bold">Multi-Agent Simulation Center</h1>
      </div>

      <Section title="Agent network — live interactions">
        <div className="relative h-80">
          <svg viewBox="0 0 600 320" className="h-full w-full">
            {agents.map((a, i) => {
              const angle = (i / agents.length) * Math.PI * 2;
              const x = 300 + Math.cos(angle) * 110, y = 160 + Math.sin(angle) * 110;
              return agents.map((_, j) => j > i && Math.random() > 0.4 ? (() => {
                const a2 = (j / agents.length) * Math.PI * 2;
                const x2 = 300 + Math.cos(a2) * 110, y2 = 160 + Math.sin(a2) * 110;
                return <line key={`${i}-${j}`} x1={x} y1={y} x2={x2} y2={y2} stroke="var(--color-cyan)" strokeWidth="0.5" opacity="0.3" />;
              })() : null);
            })}
            <circle cx="300" cy="160" r="30" fill="url(#core)" />
            <defs><radialGradient id="core"><stop offset="0%" stopColor="var(--color-cyan)" /><stop offset="100%" stopColor="var(--color-purple)" /></radialGradient></defs>
            <text x="300" y="164" textAnchor="middle" className="fill-background text-[10px] font-bold">CORE</text>
            {agents.map((a, i) => {
              const angle = (i / agents.length) * Math.PI * 2;
              const x = 300 + Math.cos(angle) * 110, y = 160 + Math.sin(angle) * 110;
              return (<g key={a.n}>
                <circle cx={x} cy={y} r="14" fill={a.s === "active" ? "var(--color-cyan)" : "var(--color-muted-foreground)"} opacity="0.8" />
                <text x={x} y={y + 3} textAnchor="middle" className="fill-background text-[9px] font-bold">{a.n.slice(0, 2)}</text>
                <text x={x} y={y + 30} textAnchor="middle" className="fill-muted-foreground text-[10px]">{a.n}</text>
              </g>);
            })}
          </svg>
        </div>
      </Section>

      <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-4">
        {agents.map((a) => (
          <div key={a.n} className="glass rounded-xl p-4">
            <div className="mb-2 flex items-center justify-between"><div className="font-mono text-sm">{a.n}</div><Badge tone={a.s === "active" ? "success" : "cyan"}>{a.s}</Badge></div>
            <div className="text-xs text-muted-foreground">{a.d}</div>
            <div className="mt-3 text-[10px] text-muted-foreground">Load {a.l}%</div>
            <div className="mt-1 h-1 rounded-full bg-muted overflow-hidden"><div className="h-full rounded-full bg-gradient-to-r from-cyan to-purple" style={{ width: `${a.l}%` }} /></div>
          </div>
        ))}
      </div>
    </div>
  );
}
