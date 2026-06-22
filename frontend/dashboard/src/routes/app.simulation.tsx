import { createFileRoute, Link } from "@tanstack/react-router";
import { Section, Badge } from "@/components/wynthora";
import { Cpu } from "lucide-react";

export const Route = createFileRoute("/app/simulation")({ component: Sim });

function Sim() {
  const stages = [
    ["Data ingestion", 100],
    ["Agent initialization", 100],
    ["Monte Carlo iterations", 64],
    ["Ensemble convergence", 12],
    ["Result synthesis", 0],
  ] as const;
  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-widest text-muted-foreground">Sim #WYN-A14 · running</p>
          <h1 className="font-display text-3xl font-bold">EU-CN Tariff Cascade</h1>
        </div>
        <div className="flex gap-2"><Badge tone="cyan">live</Badge><Badge>250K iterations</Badge><Badge tone="purple">42 agents</Badge></div>
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        <Section title="Progress" className="lg:col-span-2">
          <div className="space-y-4">
            {stages.map(([n, p]) => (
              <div key={n}>
                <div className="mb-1 flex justify-between text-xs"><span>{n}</span><span className="font-mono text-muted-foreground">{p}%</span></div>
                <div className="h-1.5 rounded-full bg-muted overflow-hidden"><div className="h-full rounded-full bg-gradient-to-r from-cyan to-purple transition-all" style={{ width: `${p}%` }} /></div>
              </div>
            ))}
          </div>
          <div className="mt-6 grid grid-cols-4 gap-2 text-center text-xs">
            {[["Elapsed", "08:42"], ["ETA", "05:18"], ["Iter/s", "478"], ["GPU util", "94%"]].map(([l, v]) => (
              <div key={l} className="glass rounded-lg p-3"><div className="text-muted-foreground">{l}</div><div className="mt-1 font-mono text-lg">{v}</div></div>
            ))}
          </div>
        </Section>

        <Section title="Agent activity">
          <ul className="space-y-2 text-xs">
            {[
              ["Macro Agent", "computing inflation pass-through", "success"],
              ["Geo Agent", "evaluating retaliation paths", "cyan"],
              ["FX Agent", "calibrating EUR/USD vol surface", "purple"],
              ["Energy Agent", "stress-testing Brent", "warning"],
              ["Trade Agent", "modeling re-routing", "success"],
            ].map(([n, a, t]) => (
              <li key={n} className="glass flex items-center gap-2 rounded-lg border border-border p-2">
                <span className={`h-2 w-2 shrink-0 rounded-full bg-${t} animate-pulse`} style={{ background: `var(--color-${t})` }} />
                <div className="min-w-0 flex-1"><div className="truncate font-medium">{n}</div><div className="truncate text-muted-foreground">{a}</div></div>
              </li>
            ))}
          </ul>
        </Section>
      </div>

      <Section title="Live logs" action={<Cpu className="h-4 w-4 text-cyan" />}>
        <pre className="max-h-72 overflow-y-auto rounded-lg border border-border bg-black/40 p-4 font-mono text-[11px] leading-relaxed text-muted-foreground">
{`[08:34:11] orchestrator: scenario WYN-A14 accepted
[08:34:12] data: ingested 184 sources (47.3 GB)
[08:34:18] agents: 42/42 online
[08:34:22] mc: spawned 16 worker pools across 4 nodes
[08:35:04] macro-7: prior calibrated against 2008/2018 episodes
[08:36:21] geo-3: detecting regime: protectionist (P=0.68)
[08:37:50] mc: 50,000 / 250,000 iterations complete
[08:39:11] fx-2: EUR/USD distribution skew = -0.42
[08:40:33] energy-1: brent fat-tail risk = elevated
[08:41:55] mc: 160,000 / 250,000 iterations complete
[08:42:18] ensemble: cross-agent agreement = 0.81 ✓`}
        </pre>
      </Section>

      <div className="flex justify-end gap-2"><button className="glass rounded-lg border border-border px-4 py-2 text-sm">Pause</button><Link to="/app/results" className="rounded-lg bg-gradient-to-r from-cyan to-purple px-5 py-2 text-sm font-semibold text-background">Preview partial results →</Link></div>
    </div>
  );
}
