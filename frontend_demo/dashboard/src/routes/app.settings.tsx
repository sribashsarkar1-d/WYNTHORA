import { createFileRoute } from "@tanstack/react-router";
import { Section, Badge } from "@/components/wynthora";
import { Copy, Eye } from "lucide-react";

export const Route = createFileRoute("/app/settings")({ component: Settings });

function Settings() {
  return (
    <div className="space-y-4">
      <div><p className="text-xs uppercase tracking-widest text-muted-foreground">Personal · Workspace</p><h1 className="font-display text-3xl font-bold">Settings</h1></div>
      <div className="grid gap-4 lg:grid-cols-[200px_1fr]">
        <nav className="space-y-1 text-sm">
          {["Profile", "Security", "API Keys", "Preferences", "Billing", "Notifications"].map((s, i) => (
            <button key={s} className={`block w-full rounded-lg px-3 py-2 text-left ${i === 0 ? "bg-white/10 text-foreground" : "text-muted-foreground hover:bg-white/5"}`}>{s}</button>
          ))}
        </nav>
        <div className="space-y-4">
          <Section title="Profile">
            <div className="flex items-center gap-4">
              <div className="grid h-16 w-16 place-items-center rounded-full bg-gradient-to-br from-cyan to-purple text-xl font-bold text-background">JC</div>
              <div><div className="font-semibold">Dr. Jane Chen</div><div className="text-xs text-muted-foreground">jane.chen@meridian.gov · Sovereign Analyst</div></div>
              <button className="ml-auto glass rounded-lg border border-border px-3 py-1.5 text-xs">Edit</button>
            </div>
          </Section>
          <Section title="Security">
            <div className="space-y-3 text-sm">
              {[["Multi-factor authentication", "TOTP · YubiKey", "success"], ["Session timeout", "15 minutes", "cyan"], ["Hardware-key required", "Enforced", "success"], ["Last login", "2 min ago · 192.168.4.21", "cyan"]].map(([k, v, t]) => (
                <div key={k} className="flex items-center justify-between border-b border-border py-2"><div><div>{k}</div><div className="text-xs text-muted-foreground">{v}</div></div><Badge tone={t as any}>{t === "success" ? "on" : "info"}</Badge></div>
              ))}
            </div>
          </Section>
          <Section title="API keys">
            <div className="glass flex items-center gap-2 rounded-lg border border-border p-3 font-mono text-xs">
              <span className="flex-1 truncate">sk_wyn_••••••••••••••••••••••••a47c</span>
              <button className="rounded p-1.5 hover:bg-white/10"><Eye className="h-3.5 w-3.5" /></button>
              <button className="rounded p-1.5 hover:bg-white/10"><Copy className="h-3.5 w-3.5" /></button>
              <Badge tone="success">live</Badge>
            </div>
            <button className="mt-3 text-xs text-cyan hover:underline">+ Generate new key</button>
          </Section>
        </div>
      </div>
    </div>
  );
}
