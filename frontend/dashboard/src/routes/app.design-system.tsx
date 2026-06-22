import { createFileRoute } from "@tanstack/react-router";
import { Section, Badge, StatCard, Spark } from "@/components/wynthora";
import { ChevronDown, Search, Sparkles } from "lucide-react";

export const Route = createFileRoute("/app/design-system")({ component: DS });

function DS() {
  return (
    <div className="space-y-6">
      <div><p className="text-xs uppercase tracking-widest text-muted-foreground">Foundations · Components · Patterns</p><h1 className="font-display text-3xl font-bold">WYNTHORA Design System</h1></div>

      <Section title="Color tokens">
        <div className="grid grid-cols-3 gap-3 md:grid-cols-6">
          {[["background", "#060814"], ["primary / cyan", "#00D4FF"], ["accent / purple", "#7C3AED"], ["success", "emerald"], ["warning", "amber"], ["danger", "red"]].map(([n, h]) => (
            <div key={n} className="glass overflow-hidden rounded-xl">
              <div className="h-20" style={{ background: n.includes("cyan") ? "var(--color-cyan)" : n.includes("purple") ? "var(--color-purple)" : n.includes("success") ? "var(--color-success)" : n.includes("warning") ? "var(--color-warning)" : n.includes("danger") ? "var(--color-destructive)" : "#060814" }} />
              <div className="p-3 text-xs"><div className="font-medium">{n}</div><div className="font-mono text-muted-foreground">{h}</div></div>
            </div>
          ))}
        </div>
      </Section>

      <Section title="Typography">
        <div className="space-y-3">
          <div><div className="font-display text-5xl font-bold tracking-tight">Display / 60 / Bold</div><div className="text-xs text-muted-foreground">SF Pro Display · Inter</div></div>
          <div className="text-3xl font-semibold">Heading / 30 / Semibold</div>
          <div className="text-base">Body — Inter regular. The reasoning fabric powers every prediction.</div>
          <div className="font-mono text-sm text-cyan">{"// mono — JetBrains, used for numerics & code"}</div>
        </div>
      </Section>

      <Section title="Buttons">
        <div className="flex flex-wrap gap-3">
          <button className="rounded-lg bg-gradient-to-r from-cyan to-purple px-5 py-2.5 text-sm font-semibold text-background glow-cyan">Primary</button>
          <button className="glass rounded-lg border border-border px-5 py-2.5 text-sm font-semibold">Secondary</button>
          <button className="rounded-lg border border-cyan/40 px-5 py-2.5 text-sm text-cyan">Outline</button>
          <button className="rounded-lg px-5 py-2.5 text-sm text-muted-foreground hover:text-foreground">Ghost</button>
          <button className="rounded-lg bg-destructive px-5 py-2.5 text-sm font-semibold text-background">Destructive</button>
        </div>
      </Section>

      <Section title="Inputs">
        <div className="grid gap-3 md:grid-cols-2">
          <div className="glass flex items-center gap-2 rounded-lg border border-border px-3"><Search className="h-4 w-4 text-muted-foreground" /><input className="h-10 w-full bg-transparent text-sm focus:outline-none" placeholder="Text input" /></div>
          <div className="glass flex items-center justify-between rounded-lg border border-border px-3 py-2.5 text-sm"><span>Dropdown</span><ChevronDown className="h-4 w-4" /></div>
        </div>
      </Section>

      <Section title="Cards & stats">
        <div className="grid gap-3 md:grid-cols-3">
          <StatCard label="metric" value="$108.4T" delta="+2.4%" data={Array.from({ length: 20 }, (_, i) => 50 + Math.sin(i) * 20)} />
          <StatCard label="metric" value="6.8" delta="+0.3" data={Array.from({ length: 20 }, (_, i) => 50 + Math.cos(i) * 25)} color="var(--color-purple)" />
          <StatCard label="metric" value="94%" data={Array.from({ length: 20 }, (_, i) => 70 + Math.sin(i / 2) * 15)} color="var(--color-success)" />
        </div>
      </Section>

      <Section title="Badges">
        <div className="flex flex-wrap gap-2">
          <Badge>cyan</Badge><Badge tone="purple">purple</Badge><Badge tone="success">success</Badge><Badge tone="warning">warning</Badge><Badge tone="danger">danger</Badge>
        </div>
      </Section>

      <Section title="Charts">
        <div className="grid gap-3 md:grid-cols-3">
          <div className="glass rounded-xl p-3"><Spark data={Array.from({ length: 24 }, (_, i) => 50 + Math.sin(i / 2) * 20)} h={80} /></div>
          <div className="glass rounded-xl p-3"><Spark data={Array.from({ length: 24 }, (_, i) => 50 + Math.cos(i / 3) * 25)} h={80} color="var(--color-purple)" /></div>
          <div className="glass rounded-xl p-3"><Spark data={Array.from({ length: 24 }, (_, i) => 30 + i)} h={80} color="var(--color-success)" /></div>
        </div>
      </Section>

      <Section title="Modal preview">
        <div className="glass mx-auto max-w-md rounded-2xl border border-cyan/30 p-6 glow-cyan">
          <div className="flex items-center gap-2"><Sparkles className="h-5 w-5 text-cyan" /><h3 className="font-semibold">Confirm simulation</h3></div>
          <p className="mt-2 text-sm text-muted-foreground">Run 250,000 iterations across 42 agents? Estimated cost: $284.</p>
          <div className="mt-4 flex justify-end gap-2"><button className="rounded-lg border border-border px-4 py-2 text-sm">Cancel</button><button className="rounded-lg bg-gradient-to-r from-cyan to-purple px-4 py-2 text-sm font-semibold text-background">Run</button></div>
        </div>
      </Section>
    </div>
  );
}
