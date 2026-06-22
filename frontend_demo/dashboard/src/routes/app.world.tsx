import { createFileRoute } from "@tanstack/react-router";
import { Section, Badge, Globe } from "@/components/wynthora";

export const Route = createFileRoute("/app/world")({ component: World });

function World() {
  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-widest text-muted-foreground">Interactive · Real-time</p>
          <h1 className="font-display text-3xl font-bold">World Map</h1>
        </div>
        <div className="glass flex gap-1 rounded-lg border border-border p-1 text-xs">
          {["Economy", "Climate", "Trade routes", "Conflicts"].map((l, i) => (
            <button key={l} className={`rounded-md px-3 py-1.5 ${i === 0 ? "bg-cyan/20 text-cyan" : "text-muted-foreground"}`}>{l}</button>
          ))}
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-[1fr_320px]">
        <div className="glass rounded-xl p-6">
          <div className="grid place-items-center"><Globe size={520} /></div>
        </div>
        <div className="space-y-4">
          <Section title="Selected: Germany">
            <dl className="space-y-2 text-sm">
              {[["GDP", "$4.5T"], ["Pop.", "84.5M"], ["Risk", "4.1 / 10"], ["Climate", "+1.7°C"], ["Trade balance", "+€213B"]].map(([k, v]) => (
                <div key={k} className="flex justify-between border-b border-border py-1.5 text-xs"><dt className="text-muted-foreground">{k}</dt><dd className="font-mono">{v}</dd></div>
              ))}
            </dl>
            <div className="mt-3"><Badge tone="success">stable</Badge> <Badge tone="warning">energy-exposed</Badge></div>
          </Section>
          <Section title="Layers">
            <ul className="space-y-2 text-xs">
              {["Economic indicators", "Climate models", "Trade routes", "Conflict zones", "Migration", "Energy grid"].map((l, i) => (
                <li key={l} className="flex items-center justify-between"><label className="flex items-center gap-2"><input type="checkbox" defaultChecked={i < 3} className="accent-cyan" />{l}</label><span className="text-muted-foreground">{Math.round(Math.random() * 100)}</span></li>
              ))}
            </ul>
          </Section>
        </div>
      </div>
    </div>
  );
}
