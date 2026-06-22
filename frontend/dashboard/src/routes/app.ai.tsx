import { createFileRoute } from "@tanstack/react-router";
import { Section, Badge } from "@/components/wynthora";
import { Bot, Send, Sparkles, User } from "lucide-react";

export const Route = createFileRoute("/app/ai")({ component: AI });

function AI() {
  return (
    <div className="grid gap-4 lg:grid-cols-[1fr_320px]">
      <div className="glass flex h-[calc(100vh-7rem)] flex-col rounded-xl">
        <div className="flex items-center gap-3 border-b border-border p-4">
          <div className="grid h-9 w-9 place-items-center rounded-lg bg-gradient-to-br from-cyan to-purple"><Bot className="h-5 w-5 text-background" /></div>
          <div><div className="text-sm font-semibold">WYNTHORA Orchestrator</div><div className="text-xs text-muted-foreground">42 agents · Macro · Climate · Geo · FX · Trade</div></div>
          <Badge tone="success">online</Badge>
        </div>
        <div className="flex-1 space-y-6 overflow-y-auto p-6">
          <Msg who="user" text="If China imposes tariffs on EU EVs by Q3, what's the cascade effect on German GDP and Brent crude?" />
          <Msg who="ai" text={`Running multi-domain simulation across 4 agents...\n\n**Macro Agent (P=0.71)**: German GDP contracts -0.4% to -0.9% over 6 quarters. Auto sector exposure: 7.2% of GDP.\n\n**Geo Agent (P=0.64)**: EU retaliatory tariffs probable (P=0.58). WTO arbitration triggers within 90d.\n\n**Energy Agent**: Brent likely range $89–$104. Tariff inflation passes through 0.3-0.5% to oil demand.\n\nMonte Carlo (250K iter) attached. Three scenarios diverge at month 9.`} />
          <Msg who="ai" text="Would you like me to spawn a Scenario Builder pre-populated with these assumptions?" small />
        </div>
        <div className="border-t border-border p-4">
          <div className="glass flex items-end gap-2 rounded-xl border border-cyan/30 p-3">
            <textarea rows={2} className="flex-1 resize-none bg-transparent text-sm placeholder:text-muted-foreground focus:outline-none" placeholder="Ask anything. Forecast EUR. Stress-test the Suez. Model a Fed pause..." />
            <button className="rounded-lg bg-gradient-to-r from-cyan to-purple p-2 text-background"><Send className="h-4 w-4" /></button>
          </div>
          <div className="mt-2 flex flex-wrap gap-2 text-xs">
            {["Forecast inflation", "Compare 3 scenarios", "Build geopolitical brief", "Detect anomalies"].map((s) => (
              <button key={s} className="glass rounded-full border border-border px-3 py-1 text-muted-foreground hover:text-foreground">{s}</button>
            ))}
          </div>
        </div>
      </div>

      <div className="space-y-4">
        <Section title="Recommendations" action={<Sparkles className="h-4 w-4 text-purple" />}>
          <ul className="space-y-2 text-sm">
            {["Hedge JPY exposure ahead of BoJ", "Increase Atlantic shipping monitoring", "Rebalance climate-vulnerable equities"].map((r) => (
              <li key={r} className="rounded-lg border border-border p-2.5 text-xs">{r}</li>
            ))}
          </ul>
        </Section>
        <Section title="Insights Feed">
          <ul className="space-y-2 text-xs">
            {[
              ["Agent 14 detected regime shift in copper futures", "2m ago"],
              ["New satellite data ingested (Sentinel-2)", "11m ago"],
              ["Ensemble retrained — accuracy +0.4pp", "1h ago"],
              ["Treasury auction outlier flagged", "3h ago"],
            ].map(([t, w]) => (
              <li key={t} className="border-l-2 border-cyan pl-3"><div>{t}</div><div className="text-muted-foreground">{w}</div></li>
            ))}
          </ul>
        </Section>
      </div>
    </div>
  );
}

function Msg({ who, text, small }: { who: "user" | "ai"; text: string; small?: boolean }) {
  const isUser = who === "user";
  return (
    <div className={`flex gap-3 ${isUser ? "flex-row-reverse" : ""}`}>
      <div className={`grid h-8 w-8 shrink-0 place-items-center rounded-lg ${isUser ? "bg-muted" : "bg-gradient-to-br from-cyan to-purple"}`}>
        {isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4 text-background" />}
      </div>
      <div className={`max-w-2xl rounded-2xl px-4 py-3 text-sm leading-relaxed ${isUser ? "bg-cyan/10 border border-cyan/30" : "glass"} ${small ? "italic text-muted-foreground" : ""}`}>
        {text.split("\n").map((l, i) => <div key={i}>{l || <br />}</div>)}
      </div>
    </div>
  );
}
