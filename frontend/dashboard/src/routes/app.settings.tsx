import { useState } from "react";
import { createFileRoute } from "@tanstack/react-router";
import { Section, Badge } from "@/components/wynthora";
import { Copy, Eye, CheckCircle2 } from "lucide-react";

export const Route = createFileRoute("/app/settings")({ component: Settings });

function Settings() {
  const [activeTab, setActiveTab] = useState("Profile");
  const tabs = ["Profile", "Security", "API Keys", "Preferences", "Billing", "Notifications"];

  return (
    <div className="space-y-4">
      <div><p className="text-xs uppercase tracking-widest text-muted-foreground">Personal · Workspace</p><h1 className="font-display text-3xl font-bold">Settings</h1></div>
      <div className="grid gap-4 lg:grid-cols-[200px_1fr]">
        <nav className="space-y-1 text-sm">
          {tabs.map((s) => (
            <button 
              key={s} 
              onClick={() => setActiveTab(s)}
              className={`block w-full rounded-lg px-3 py-2 text-left transition-colors ${activeTab === s ? "bg-white/10 text-foreground shadow-sm shadow-black/20 border border-white/5" : "text-muted-foreground hover:bg-white/5"}`}
            >
              {s}
            </button>
          ))}
        </nav>
        <div className="space-y-4">
          {activeTab !== "Billing" && (
            <>
              <Section title="Profile">
                <div className="flex items-center gap-4">
                  <div className="grid h-16 w-16 place-items-center rounded-full bg-gradient-to-br from-cyan to-purple text-xl font-bold text-background shadow-lg shadow-cyan/20">JC</div>
                  <div><div className="font-semibold text-lg tracking-tight">Dr. Jane Chen</div><div className="text-xs text-muted-foreground">jane.chen@meridian.gov · Sovereign Analyst</div></div>
                  <button className="ml-auto glass rounded-lg border border-border px-4 py-2 text-xs font-medium hover:bg-white/5 transition-colors">Edit Profile</button>
                </div>
              </Section>
              <Section title="Security">
                <div className="space-y-3 text-sm">
                  {[["Multi-factor authentication", "TOTP · YubiKey", "success"], ["Session timeout", "15 minutes", "cyan"], ["Hardware-key required", "Enforced", "success"], ["Last login", "2 min ago · 192.168.4.21", "cyan"]].map(([k, v, t]) => (
                    <div key={k} className="flex items-center justify-between border-b border-border/50 py-3 last:border-0"><div><div className="font-medium">{k}</div><div className="text-xs text-muted-foreground mt-0.5">{v}</div></div><Badge tone={t as any}>{t === "success" ? "on" : "info"}</Badge></div>
                  ))}
                </div>
              </Section>
              <Section title="API keys">
                <div className="glass flex items-center gap-2 rounded-lg border border-border p-3 font-mono text-xs shadow-inner">
                  <span className="flex-1 truncate text-muted-foreground">sk_wyn_••••••••••••••••••••••••a47c</span>
                  <button className="rounded p-1.5 hover:bg-white/10 transition-colors"><Eye className="h-4 w-4 text-cyan" /></button>
                  <button className="rounded p-1.5 hover:bg-white/10 transition-colors"><Copy className="h-4 w-4 text-cyan" /></button>
                  <Badge tone="success">live</Badge>
                </div>
                <button className="mt-4 text-xs font-medium text-cyan hover:text-cyan/80 transition-colors flex items-center gap-1">+ Generate new secret key</button>
              </Section>
            </>
          )}

          {activeTab === "Billing" && (
            <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <Section title="Current Plan">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan to-blue-500">Enterprise Tier</h3>
                    <p className="text-sm text-muted-foreground mt-1">Unlimited simulations · 10,000 Monte Carlo runs · Premium Support</p>
                  </div>
                  <Badge tone="success">Active</Badge>
                </div>
                <div className="mt-6 glass rounded-xl border border-border p-4">
                  <div className="flex justify-between text-sm mb-2"><span className="text-muted-foreground">Compute Usage (GPU hours)</span><span className="font-mono">842 / 1000</span></div>
                  <div className="h-2 w-full bg-black/50 rounded-full overflow-hidden border border-white/5">
                    <div className="h-full bg-gradient-to-r from-cyan to-purple w-[84%] rounded-full shadow-[0_0_10px_rgba(77,184,255,0.5)]" />
                  </div>
                </div>
                <div className="mt-6 flex gap-3">
                  <button className="rounded-lg bg-white text-black px-4 py-2 text-sm font-semibold hover:bg-white/90 transition-all shadow-lg shadow-white/10">Manage Subscription</button>
                  <button className="glass rounded-lg border border-border px-4 py-2 text-sm font-medium hover:bg-white/5 transition-colors">View Invoices</button>
                </div>
              </Section>
              
              <div className="grid gap-4 md:grid-cols-3">
                {[
                  { name: "Starter", price: "$999", desc: "For researchers and small funds.", feats: ["100 Simulations/mo", "Basic API Access", "Standard Models"] },
                  { name: "Enterprise", price: "$4,999", desc: "For Fortune 500 & Hedge Funds.", feats: ["Unlimited Simulations", "10k Monte Carlo Runs", "Real-time WebSockets", "Dedicated GPU Nodes"], active: true },
                  { name: "Government", price: "Custom", desc: "On-prem deployment for national security.", feats: ["Air-gapped Deployment", "Custom RL Agents", "Top Secret Clearance Ops", "White-glove Support"] }
                ].map(p => (
                  <div key={p.name} className={`relative glass rounded-xl border p-5 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl ${p.active ? "border-cyan shadow-cyan/10" : "border-border"}`}>
                    {p.active && <div className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-cyan px-3 py-0.5 text-[10px] font-bold uppercase text-black">Current Plan</div>}
                    <h4 className="font-semibold text-lg">{p.name}</h4>
                    <div className="mt-2 text-2xl font-bold font-mono">{p.price}<span className="text-sm font-normal text-muted-foreground">{p.price !== "Custom" ? "/mo" : ""}</span></div>
                    <p className="mt-2 text-xs text-muted-foreground h-8">{p.desc}</p>
                    <ul className="mt-4 space-y-2">
                      {p.feats.map(f => <li key={f} className="flex items-center gap-2 text-xs text-foreground/90"><CheckCircle2 className="h-3.5 w-3.5 text-cyan" /> {f}</li>)}
                    </ul>
                    <button className={`mt-6 w-full rounded-lg px-4 py-2 text-sm font-medium transition-all ${p.active ? "bg-white/10 text-white cursor-default" : "bg-cyan text-black hover:bg-cyan/90 shadow-[0_0_15px_rgba(77,184,255,0.3)]"}`}>
                      {p.active ? "Current" : "Upgrade"}
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
