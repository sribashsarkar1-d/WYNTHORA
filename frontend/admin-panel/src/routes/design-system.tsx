import { createFileRoute } from "@tanstack/react-router";
import { Panel, PageHeader, Btn, Pill } from "@/components/ui-x/Panel";

export const Route = createFileRoute("/design-system")({
  head: () => ({ meta: [{ title: "Design System — WYNTHORA" }] }),
  component: DesignSystem,
});

const tokens = [
  { name: "background", v: "oklch(0.16 0.035 260)" },
  { name: "surface",    v: "oklch(0.20 0.04 260)" },
  { name: "primary",    v: "oklch(0.82 0.15 210)" },
  { name: "secondary",  v: "oklch(0.62 0.20 295)" },
  { name: "success",    v: "oklch(0.74 0.17 155)" },
  { name: "warning",    v: "oklch(0.80 0.16 80)" },
  { name: "destructive",v: "oklch(0.66 0.24 25)" },
  { name: "border",     v: "oklch(0.32 0.04 260 / 60%)" },
];

function DesignSystem() {
  return (
    <div className="fade-in-up">
      <PageHeader
        eyebrow="Foundation"
        title="Design System"
        description="Tokens, surfaces, and components powering the WYNTHORA command panel."
      />

      <div className="grid gap-5 lg:grid-cols-2">
        <Panel title="Typography">
          <div className="space-y-3">
            <div>
              <div className="font-mono text-[10px] uppercase text-muted-foreground">Display · Space Grotesk</div>
              <div className="font-display text-3xl font-bold">Predict the world. Shape the future.</div>
            </div>
            <div>
              <div className="font-mono text-[10px] uppercase text-muted-foreground">Body · Inter</div>
              <p className="text-sm">A futures-grade interface for orchestrating planet-scale simulation, prediction, and intelligence.</p>
            </div>
            <div>
              <div className="font-mono text-[10px] uppercase text-muted-foreground">Mono · JetBrains Mono</div>
              <div className="font-mono text-xs">latency=34ms · model=geo-llm-v4.2 · iters=10⁷</div>
            </div>
          </div>
        </Panel>

        <Panel title="Color Tokens">
          <div className="grid grid-cols-4 gap-2">
            {tokens.map((t) => (
              <div key={t.name}>
                <div className="h-14 rounded-md border border-border" style={{ background: t.v }} />
                <div className="mt-1 font-mono text-[10px]">{t.name}</div>
              </div>
            ))}
          </div>
        </Panel>

        <Panel title="Buttons & Pills">
          <div className="space-y-3">
            <div className="flex flex-wrap gap-2">
              <Btn variant="primary">Primary</Btn>
              <Btn variant="default">Default</Btn>
              <Btn variant="ghost">Ghost</Btn>
              <Btn variant="danger">Danger</Btn>
            </div>
            <div className="flex flex-wrap gap-2">
              <Pill tone="primary">PRIMARY</Pill>
              <Pill tone="secondary">SECONDARY</Pill>
              <Pill tone="success">SUCCESS</Pill>
              <Pill tone="warning">WARNING</Pill>
              <Pill tone="danger">DANGER</Pill>
              <Pill tone="muted">MUTED</Pill>
            </div>
          </div>
        </Panel>

        <Panel title="Surfaces & Effects">
          <div className="grid grid-cols-2 gap-3">
            <div className="rounded-md glass p-4 text-xs">.glass</div>
            <div className="rounded-md glass-strong p-4 text-xs">.glass-strong</div>
            <div className="rounded-md p-4 text-xs grid-bg border border-border">.grid-bg</div>
            <div className="rounded-md p-4 text-xs bg-[var(--gradient-aurora)] text-primary-foreground font-semibold">aurora gradient</div>
          </div>
        </Panel>

        <Panel title="Component Library" className="lg:col-span-2">
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2 text-xs">
            {["Cards","Tables","Buttons","Inputs","Forms","Dropdowns","Charts","World Maps","Modals","Drawers","Navigation","Icons","Empty States","Loading States","Error States","Success States","Skeleton Screens","Responsive Components"].map((c) => (
              <div key={c} className="rounded-md bg-background/40 px-3 py-2.5 border border-border/50">{c}</div>
            ))}
          </div>
        </Panel>
      </div>
    </div>
  );
}
