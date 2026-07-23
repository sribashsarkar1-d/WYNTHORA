import { createFileRoute, Link } from "@tanstack/react-router";
import { Globe } from "@/components/wynthora";
import { ArrowRight, Activity, Brain, Cpu, Globe2, LineChart, Shield, Sparkles, Zap } from "lucide-react";

export const Route = createFileRoute("/")({
  head: () => ({ meta: [
    { title: "WYNTHORA — The AI World Simulation Engine" },
    { name: "description", content: "Forecast economy, climate, politics and global risk with multi-agent AI and Monte Carlo simulation. Built for governments, hedge funds, banks, and Fortune 500." },
    { property: "og:title", content: "WYNTHORA — AI World Simulation Engine" },
    { property: "og:description", content: "Enterprise-grade scenario forecasting for the next decade." },
  ] }),
  component: Landing,
});

function Landing() {
  return (
    <div className="relative min-h-screen overflow-hidden">
      {/* Nav */}
      <header className="relative z-20 flex items-center justify-between px-6 py-5 lg:px-12">
        <Link to="/" className="flex items-center gap-2">
          <div className="grid h-9 w-9 place-items-center rounded-lg bg-gradient-to-br from-cyan to-purple"><Globe2 className="h-5 w-5 text-background" /></div>
          <span className="text-lg font-bold tracking-[0.2em]">WYNTHORA</span>
        </Link>
        <nav className="hidden items-center gap-8 text-sm text-muted-foreground md:flex">
          <a href="#platform" className="hover:text-foreground">Platform</a>
          <a href="#features" className="hover:text-foreground">Capabilities</a>
          <a href="#pricing" className="hover:text-foreground">Pricing</a>
          <a href="#enterprise" className="hover:text-foreground">Enterprise</a>
        </nav>
        <div className="flex items-center gap-2">
          <Link to="/login" className="hidden rounded-lg px-3 py-2 text-sm text-muted-foreground hover:text-foreground md:inline">Sign in</Link>
          <Link to="/app/dashboard" className="glass rounded-lg border border-cyan/40 px-4 py-2 text-sm font-medium glow-cyan">Launch Console</Link>
        </div>
      </header>

      {/* Hero */}
      <section className="relative px-6 pb-32 pt-12 lg:px-12">
        <div className="grid-bg pointer-events-none absolute inset-0 opacity-40" />
        <div className="relative mx-auto grid max-w-7xl items-center gap-12 lg:grid-cols-2">
          <div>
            <div className="glass mb-6 inline-flex items-center gap-2 rounded-full border border-cyan/30 px-3 py-1 text-xs">
              <span className="h-1.5 w-1.5 rounded-full bg-cyan animate-pulse" />
              Live: 12,847 simulations running globally
            </div>
            <h1 className="font-display text-5xl font-bold leading-[1.05] tracking-tight md:text-7xl">
              Simulate the<br/><span className="text-gradient">entire world.</span>
            </h1>
            <p className="mt-6 max-w-xl text-lg text-muted-foreground">
              WYNTHORA is the AI-native world simulation engine. Forecast macroeconomies, climate trajectories, geopolitical shocks and supply chains — with multi-agent reasoning and one-million-iteration Monte Carlo precision.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link to="/app/dashboard" className="inline-flex items-center gap-2 rounded-lg bg-gradient-to-r from-cyan to-purple px-6 py-3 text-sm font-semibold text-background glow-cyan">
                Open the Engine <ArrowRight className="h-4 w-4" />
              </Link>
              <Link to="/login" className="glass inline-flex items-center gap-2 rounded-lg border border-border px-6 py-3 text-sm font-semibold">Request a Briefing</Link>
            </div>
            <div className="mt-12 grid grid-cols-3 gap-6 text-sm">
              {[["99.4%", "Forecast confidence"], ["184", "Live data sources"], ["1.2M", "Sims / day"]].map(([v, l]) => (
                <div key={l}><div className="text-2xl font-bold text-gradient">{v}</div><div className="text-xs text-muted-foreground">{l}</div></div>
              ))}
            </div>
          </div>
          <div className="relative grid place-items-center">
            <Globe size={520} />
            <div className="glass absolute -left-4 top-12 hidden rounded-xl p-3 text-xs md:block">
              <div className="text-muted-foreground">USD/CNY 24h</div>
              <div className="text-lg font-semibold text-success">7.182 ▲</div>
            </div>
            <div className="glass absolute -right-4 bottom-16 hidden rounded-xl p-3 text-xs md:block">
              <div className="text-muted-foreground">Atlantic storm prob.</div>
              <div className="text-lg font-semibold text-warning">68%</div>
            </div>
          </div>
        </div>
      </section>

      {/* Logos */}
      <section className="border-y border-border bg-background/40 px-6 py-10 backdrop-blur lg:px-12">
        <div className="mx-auto max-w-7xl">
          <p className="mb-6 text-center text-xs uppercase tracking-[0.3em] text-muted-foreground">Trusted by sovereigns, capital and industry</p>
          <div className="grid grid-cols-2 items-center gap-8 opacity-70 md:grid-cols-7">
            {["BLACKSTONE", "BRIDGEWATER", "MITSUBISHI", "ARAMCO", "BNP PARIBAS", "MERIDIAN", "ALLIANZ"].map((n) => (
              <div key={n} className="text-center font-mono text-xs tracking-[0.2em] text-muted-foreground">{n}</div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="relative px-6 py-24 lg:px-12">
        <div className="mx-auto max-w-7xl">
          <div className="mb-16 max-w-2xl">
            <p className="text-xs uppercase tracking-[0.3em] text-cyan">The Platform</p>
            <h2 className="mt-3 font-display text-4xl font-bold tracking-tight md:text-5xl">An operating system for foresight.</h2>
            <p className="mt-4 text-muted-foreground">Seven integrated modules. One reasoning fabric. Built on a federated multi-agent core that ingests, models and simulates the world in real time.</p>
          </div>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {[
              { i: Brain, t: "Multi-Agent Reasoning", d: "42 specialist agents — macro, climatology, geopolitics, supply chain — debate, dispute and converge on probabilistic answers." },
              { i: Activity, t: "Monte Carlo at Scale", d: "Run 1M+ iterations per scenario across distributed GPU clusters. Get distributions, not point estimates." },
              { i: LineChart, t: "Predictive Forecasting", d: "Hybrid LSTM/transformer ensembles trained on 50 years of global data, calibrated weekly." },
              { i: Shield, t: "Risk Intelligence", d: "Composite scoring across 197 countries. Heatmaps, matrices and early-warning systems." },
              { i: Cpu, t: "Scenario Builder", d: "Drag-and-drop assumption modeling. Stress test policy decisions before they're made." },
              { i: Zap, t: "Real-Time Alerts", d: "Sub-second event detection. Push intelligence to Bloomberg, Slack, Teams and your SOC." },
            ].map(({ i: Icon, t, d }) => (
              <div key={t} className="glass group rounded-2xl p-6 transition hover:border-cyan/40">
                <div className="mb-4 grid h-10 w-10 place-items-center rounded-lg bg-gradient-to-br from-cyan/20 to-purple/20 border border-cyan/30"><Icon className="h-5 w-5 text-cyan" /></div>
                <h3 className="text-lg font-semibold">{t}</h3>
                <p className="mt-2 text-sm text-muted-foreground">{d}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Use Cases */}
      <section className="border-y border-border bg-background/40 px-6 py-24 backdrop-blur lg:px-12">
        <div className="mx-auto max-w-7xl">
          <div className="mb-16 text-center">
            <p className="text-xs uppercase tracking-[0.3em] text-cyan">Who it's for</p>
            <h2 className="mt-3 font-display text-4xl font-bold tracking-tight md:text-5xl">Built for decision makers.</h2>
          </div>
          <div className="grid gap-6 md:grid-cols-3">
            {[
              { t: "Hedge Funds", d: "Simulate market reactions to geopolitical shocks before they happen. Alpha generation via alternative data." },
              { t: "Governments", d: "Stress-test policy decisions against macroeconomic and climate scenarios to ensure national resilience." },
              { t: "Supply Chain Leaders", d: "Identify vulnerabilities in global logistics networks and automatically route around disruptions." }
            ].map(({ t, d }) => (
              <div key={t} className="glass rounded-2xl p-8 border-t-4 border-t-cyan hover:border-cyan/50 transition">
                <h3 className="text-xl font-bold">{t}</h3>
                <p className="mt-4 text-sm text-muted-foreground">{d}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it Works */}
      <section className="px-6 py-24 lg:px-12">
        <div className="mx-auto max-w-7xl">
          <div className="mb-16 max-w-2xl">
            <p className="text-xs uppercase tracking-[0.3em] text-cyan">The Pipeline</p>
            <h2 className="mt-3 font-display text-4xl font-bold tracking-tight md:text-5xl">From raw data to foresight.</h2>
          </div>
          <div className="relative border-l border-border/50 pl-8 ml-4 space-y-12">
            {[
              { s: "01", t: "Ingest Global Data", d: "Connect to 180+ real-time feeds including satellite imagery, financial markets, and news sentiment." },
              { s: "02", t: "Multi-Agent Simulation", d: "Our 42 AI agents run thousands of Monte Carlo iterations to map out probability distributions of future events." },
              { s: "03", t: "Actionable Insights", d: "Receive clear, probabilistic forecasts directly in your dashboard or integrated into your existing workflows." }
            ].map(({ s, t, d }) => (
              <div key={s} className="relative">
                <div className="absolute -left-12 top-0 flex h-8 w-8 items-center justify-center rounded-full bg-cyan/20 text-xs font-bold text-cyan ring-4 ring-background">{s}</div>
                <h3 className="text-xl font-bold text-foreground">{t}</h3>
                <p className="mt-2 max-w-xl text-muted-foreground">{d}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="px-6 py-24 lg:px-12">
        <div className="mx-auto max-w-7xl">
          <div className="mb-12 text-center">
            <p className="text-xs uppercase tracking-[0.3em] text-cyan">Pricing</p>
            <h2 className="mt-3 font-display text-4xl font-bold md:text-5xl">License the engine.</h2>
          </div>
          <div className="grid gap-6 md:grid-cols-3">
            {[
              { n: "Analyst", p: "$2,400", per: "/seat / mo", f: ["10K sims / month", "5 active scenarios", "Standard data sources", "Email & Slack alerts"], cta: "Start trial" },
              { n: "Institutional", p: "$28K", per: "/mo", f: ["Unlimited sims", "100 scenarios", "Premium tier-1 data", "Multi-agent customization", "Dedicated success engineer"], cta: "Talk to sales", featured: true },
              { n: "Sovereign", p: "Custom", per: "", f: ["On-premise deployment", "Air-gapped option", "Custom agents & sources", "SOC 2 + FedRAMP High", "24/7 white-glove SLA"], cta: "Contact us" },
            ].map((t) => (
              <div key={t.n} className={`glass relative rounded-2xl p-8 ${t.featured ? "border-cyan/50 glow-cyan" : ""}`}>
                {t.featured && <div className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-gradient-to-r from-cyan to-purple px-3 py-1 text-xs font-semibold text-background">Most chosen</div>}
                <div className="text-sm text-muted-foreground">{t.n}</div>
                <div className="mt-2 flex items-baseline gap-1"><span className="text-4xl font-bold">{t.p}</span><span className="text-sm text-muted-foreground">{t.per}</span></div>
                <ul className="mt-6 space-y-2 text-sm">{t.f.map((x) => <li key={x} className="flex gap-2"><Sparkles className="h-4 w-4 shrink-0 text-cyan" />{x}</li>)}</ul>
                <button className={`mt-8 w-full rounded-lg py-2.5 text-sm font-semibold ${t.featured ? "bg-gradient-to-r from-cyan to-purple text-background" : "border border-border"}`}>{t.cta}</button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="px-6 py-24 lg:px-12">
        <div className="mx-auto grid max-w-7xl gap-6 md:grid-cols-3">
          {[
            { q: "WYNTHORA called the supply-chain shock 14 weeks before our internal desk. It paid for itself in a single quarter.", n: "Mara Iversen", r: "CIO, Nordic Sovereign Wealth" },
            { q: "The multi-agent layer is unlike anything else on the market. It actually argues with itself — and we trust the verdict.", n: "Anand Krishnan", r: "Head of Macro, Citadel" },
            { q: "We brief the cabinet from WYNTHORA. The climate-political coupling is a national-security asset.", n: "Col. R. Maddox", r: "Strategic Foresight Unit" },
          ].map((t) => (
            <figure key={t.n} className="glass rounded-2xl p-6">
              <blockquote className="text-sm leading-relaxed">"{t.q}"</blockquote>
              <figcaption className="mt-4 border-t border-border pt-4 text-xs"><div className="font-semibold">{t.n}</div><div className="text-muted-foreground">{t.r}</div></figcaption>
            </figure>
          ))}
        </div>
      </section>

      {/* FAQ */}
      <section className="border-t border-border px-6 py-24 lg:px-12">
        <div className="mx-auto max-w-3xl">
          <div className="mb-12 text-center">
            <h2 className="font-display text-3xl font-bold md:text-4xl">Frequently asked questions</h2>
          </div>
          <div className="space-y-4">
            {[
              { q: "How does WYNTHORA's multi-agent system work?", a: "We use a federated system of 42 specialized AI agents. Each agent represents a different domain (e.g., energy, geopolitics, finance). They interact and negotiate with each other during simulations to produce realistic outcomes." },
              { q: "Can I bring my own data?", a: "Yes, Institutional and Sovereign tiers support secure integrations with proprietary data lakes and internal APIs." },
              { q: "What happens if a simulation runs out of bounds?", a: "Our system flags outlier scenarios and assigns them low probabilities, while providing a full traceback of the events that led to the anomaly." },
              { q: "Is on-premise deployment available?", a: "Yes. For our Sovereign clients, we offer fully air-gapped deployments to meet strict compliance and security requirements." }
            ].map(({ q, a }) => (
              <details key={q} className="glass group rounded-xl [&_summary::-webkit-details-marker]:hidden">
                <summary className="cursor-pointer px-6 py-4 font-semibold outline-none flex justify-between items-center">
                  {q}
                  <span className="text-cyan group-open:rotate-45 transition-transform duration-200 text-2xl leading-none">+</span>
                </summary>
                <div className="px-6 pb-4 text-sm text-muted-foreground">{a}</div>
              </details>
            ))}
          </div>
        </div>
      </section>

      {/* Enterprise CTA */}
      <section id="enterprise" className="px-6 pb-24 lg:px-12">
        <div className="glass mx-auto max-w-7xl overflow-hidden rounded-3xl border border-cyan/30 p-12 text-center" style={{ background: "radial-gradient(ellipse at center, oklch(0.30 0.15 260 / 0.5), transparent 70%)" }}>
          <h2 className="font-display text-4xl font-bold md:text-5xl">Deploy the engine inside your institution.</h2>
          <p className="mx-auto mt-4 max-w-2xl text-muted-foreground">Air-gapped, sovereign-cloud, or hybrid. WYNTHORA ships with your data classifications, your auditors and your SLAs.</p>
          <div className="mt-8 flex justify-center gap-3">
            <button className="rounded-lg bg-gradient-to-r from-cyan to-purple px-6 py-3 text-sm font-semibold text-background glow-cyan">Book executive briefing</button>
            <Link to="/app/dashboard" className="glass rounded-lg border border-border px-6 py-3 text-sm font-semibold">Explore live demo</Link>
          </div>
        </div>
      </section>

      <footer className="border-t border-border px-6 py-8 text-xs text-muted-foreground lg:px-12">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4">
          <div>© {new Date().getFullYear()} WYNTHORA Labs Inc. — All forecasts are probabilistic.</div>
          <div className="flex gap-6"><a>Security</a><a>Compliance</a><a>Research</a><a>Careers</a></div>
        </div>
      </footer>
    </div>
  );
}
