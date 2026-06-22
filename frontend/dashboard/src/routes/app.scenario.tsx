import { createFileRoute, Link } from "@tanstack/react-router";
import { Section, Badge } from "@/components/wynthora";
import { Sliders, Play, Globe2, Calendar, Layers } from "lucide-react";

export const Route = createFileRoute("/app/scenario")({ component: Scenario });

function Scenario() {
  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-widest text-muted-foreground">New Scenario</p>
          <h1 className="font-display text-3xl font-bold">Scenario Builder</h1>
        </div>
        <Link to="/app/simulation" className="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-cyan to-purple px-5 py-2.5 text-sm font-semibold text-background glow-cyan"><Play className="h-4 w-4" /> Run simulation</Link>
      </div>

      <div className="grid gap-4 lg:grid-cols-[1fr_320px]">
        <div className="space-y-4">
          <Section title="1 · Domain selection" action={<Layers className="h-4 w-4 text-cyan" />}>
            <div className="grid grid-cols-2 gap-2 md:grid-cols-4">
              {[["Economy", true], ["Climate", true], ["Geopolitics", true], ["Trade", false], ["Energy", false], ["Health", false], ["Demographics", false], ["Tech", false]].map(([d, on]) => (
                <button key={d as string} className={`glass rounded-lg border p-3 text-sm ${on ? "border-cyan/50 text-cyan glow-cyan" : "border-border text-muted-foreground"}`}>{d}</button>
              ))}
            </div>
          </Section>

          <Section title="2 · Geography" action={<Globe2 className="h-4 w-4 text-cyan" />}>
            <div className="flex flex-wrap gap-2">
              {["Germany ×", "China ×", "United States ×", "Brazil ×", "+ add country"].map((c) => (
                <span key={c} className="glass rounded-full border border-cyan/30 px-3 py-1 text-xs">{c}</span>
              ))}
            </div>
          </Section>

          <Section title="3 · Time horizon" action={<Calendar className="h-4 w-4 text-cyan" />}>
            <div className="flex items-center gap-3">
              <input type="range" defaultValue="60" className="flex-1 accent-cyan" />
              <div className="glass rounded-lg border border-border px-3 py-1 text-sm font-mono">2025 → 2030</div>
            </div>
            <div className="mt-2 flex justify-between text-[10px] text-muted-foreground"><span>Q1 2025</span><span>5 years</span><span>Q4 2050</span></div>
          </Section>

          <Section title="4 · Variables & assumptions" action={<Sliders className="h-4 w-4 text-cyan" />}>
            <div className="space-y-3">
              {[
                ["Fed funds rate trajectory", "neutral → 3.5% by 2027"],
                ["China GDP growth", "4.2% baseline"],
                ["Brent crude floor", "$72 / barrel"],
                ["Carbon price (EU ETS)", "€95 → €140"],
                ["EUR/USD volatility", "implied +15%"],
              ].map(([v, val]) => (
                <div key={v} className="glass flex items-center gap-3 rounded-lg border border-border p-3">
                  <div className="flex-1"><div className="text-sm">{v}</div><div className="text-xs text-muted-foreground">{val}</div></div>
                  <input type="range" defaultValue="50" className="w-32 accent-cyan" />
                </div>
              ))}
            </div>
          </Section>

          <Section title="5 · Advanced parameters">
            <div className="grid grid-cols-2 gap-3 text-sm md:grid-cols-4">
              {[["Iterations", "250,000"], ["Agents", "42"], ["Confidence", "95%"], ["Seed", "0xWYN-A14"]].map(([l, v]) => (
                <div key={l} className="glass rounded-lg border border-border p-3"><div className="text-xs text-muted-foreground">{l}</div><div className="mt-1 font-mono">{v}</div></div>
              ))}
            </div>
          </Section>
        </div>

        <aside className="space-y-4">
          <Section title="Scenario summary">
            <dl className="space-y-2 text-sm">
              <Row k="Name" v="EU-CN Tariff Cascade" />
              <Row k="Domains" v="4" />
              <Row k="Countries" v="4" />
              <Row k="Horizon" v="2025–2030" />
              <Row k="Compute" v="~14 min" />
              <Row k="Cost est." v="$284" />
            </dl>
            <div className="mt-3 flex flex-wrap gap-1.5"><Badge>ready</Badge><Badge tone="purple">multi-agent</Badge><Badge tone="warning">stress-test</Badge></div>
          </Section>
          <Section title="Templates">
            <ul className="space-y-1 text-xs">
              {["Recession 2026", "Climate +2°C", "OPEC supply cut", "Cyber black swan", "BRICS expansion"].map((t) => (
                <li key={t} className="cursor-pointer rounded-lg border border-border p-2 hover:border-cyan/40">{t}</li>
              ))}
            </ul>
          </Section>
        </aside>
      </div>
    </div>
  );
}

function Row({ k, v }: { k: string; v: string }) { return <div className="flex justify-between border-b border-border py-1.5 text-xs"><dt className="text-muted-foreground">{k}</dt><dd className="font-mono">{v}</dd></div>; }
