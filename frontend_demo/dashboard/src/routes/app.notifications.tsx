import { createFileRoute } from "@tanstack/react-router";
import { Section, Badge } from "@/components/wynthora";
import { AlertTriangle, Bell, Sparkles } from "lucide-react";

export const Route = createFileRoute("/app/notifications")({ component: N });

function N() {
  const items = [
    { i: AlertTriangle, t: "Red Sea shipping risk elevated to CRITICAL", w: "2 min ago", tone: "danger" as const, c: "Risk Center" },
    { i: Sparkles, t: "AI: New regime detected in copper futures", w: "14 min ago", tone: "purple" as const, c: "Macro-7" },
    { i: AlertTriangle, t: "Pacific typhoon formation — shipping rerouted", w: "1 hr ago", tone: "warning" as const, c: "Climate-12" },
    { i: Bell, t: "Sim WYN-A14 completed (87.4% confidence)", w: "3 hr ago", tone: "success" as const, c: "Orchestrator" },
    { i: Sparkles, t: "Recommendation: hedge JPY ahead of BoJ", w: "5 hr ago", tone: "cyan" as const, c: "FX-2" },
  ];
  return (
    <div className="space-y-4">
      <div><p className="text-xs uppercase tracking-widest text-muted-foreground">Real-time · 184 sources</p><h1 className="font-display text-3xl font-bold">Notification Center</h1></div>
      <div className="flex gap-2 text-xs">{["All", "Risk", "AI", "Sims", "System"].map((f, i) => <button key={f} className={`glass rounded-full border px-3 py-1.5 ${i === 0 ? "border-cyan/50 text-cyan" : "border-border text-muted-foreground"}`}>{f}</button>)}</div>
      <Section>
        <ul className="space-y-2">
          {items.map((n, i) => (
            <li key={i} className="glass flex items-start gap-3 rounded-xl p-4">
              <div className={`grid h-9 w-9 shrink-0 place-items-center rounded-lg border`} style={{ borderColor: `var(--color-${n.tone === "danger" ? "destructive" : n.tone})`, color: `var(--color-${n.tone === "danger" ? "destructive" : n.tone})` }}><n.i className="h-4 w-4" /></div>
              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium">{n.t}</div>
                <div className="mt-1 flex items-center gap-2 text-xs text-muted-foreground"><span>{n.c}</span>·<span>{n.w}</span></div>
              </div>
              <Badge tone={n.tone}>{n.tone === "danger" ? "critical" : n.tone === "warning" ? "warning" : n.tone === "success" ? "ok" : "info"}</Badge>
            </li>
          ))}
        </ul>
      </Section>
    </div>
  );
}
