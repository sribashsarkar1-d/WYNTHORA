import { createFileRoute } from "@tanstack/react-router";
import { Section, StatCard } from "@/components/wynthora";
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line, CartesianGrid } from 'recharts';

export const Route = createFileRoute("/app/monte-carlo")({ component: MC });

const s = (n: number) => Array.from({ length: 30 }, (_, i) => 50 + Math.sin(i / 2 + n) * 20);

// Generate dummy distribution data
const distData = Array.from({ length: 60 }, (_, i) => {
  const value = (i - 30) / 5; // -6 to +6 %
  const prob = Math.exp(-Math.pow(value, 2) / 2) * 100 + Math.random() * 5;
  return { value: value.toFixed(1) + '%', probability: prob };
});

// Generate dummy convergence data
const convData = Array.from({ length: 100 }, (_, i) => ({
  iteration: i * 10,
  scenarioA: 2.5 + Math.sin(i/10) * Math.exp(-i/20),
  scenarioB: 1.2 + Math.cos(i/8) * Math.exp(-i/25),
  scenarioC: -0.5 + Math.sin(i/5) * Math.exp(-i/15)
}));

function MC() {
  return (
    <div className="space-y-4">
      <div>
        <p className="text-xs uppercase tracking-widest text-muted-foreground">Stochastic engine</p>
        <h1 className="font-display text-3xl font-bold">Monte Carlo Dashboard</h1>
      </div>
      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <StatCard label="Iterations" value="1,000,000" data={s(1)} />
        <StatCard label="Convergence" value="0.997" data={s(2)} color="var(--color-success)" />
        <StatCard label="CI width 95%" value="±1.8%" data={s(3)} color="var(--color-purple)" />
        <StatCard label="Outliers" value="0.04%" data={s(4)} color="var(--color-warning)" />
      </div>

      <Section title="Distribution of outcomes (GDP Growth)">
        <div className="h-[240px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={distData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="colorProb" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#4db8ff" stopOpacity={0.8}/>
                  <stop offset="95%" stopColor="#4db8ff" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <XAxis dataKey="value" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
              <YAxis hide />
              <Tooltip 
                contentStyle={{ backgroundColor: 'rgba(13, 17, 23, 0.9)', border: '1px solid #30363d', borderRadius: '8px' }}
                itemStyle={{ color: '#4db8ff' }}
              />
              <Area type="monotone" dataKey="probability" stroke="#4db8ff" fillOpacity={1} fill="url(#colorProb)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
        <div className="mt-2 flex justify-between px-10 text-[10px] uppercase tracking-wider text-muted-foreground">
          <span className="text-destructive">P5: -2.4%</span>
          <span className="text-cyan">Mean: +0.4%</span>
          <span className="text-success">P95: +1.2%</span>
        </div>
      </Section>

      <div className="grid gap-4 lg:grid-cols-2">
        <Section title="Iteration convergence">
          <div className="h-[180px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={convData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#30363d" vertical={false} />
                <XAxis dataKey="iteration" stroke="#888888" fontSize={10} tickLine={false} axisLine={false} />
                <YAxis stroke="#888888" fontSize={10} tickLine={false} axisLine={false} domain={[-2, 4]} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'rgba(13, 17, 23, 0.9)', border: '1px solid #30363d', borderRadius: '8px' }}
                />
                <Line type="monotone" dataKey="scenarioA" stroke="#4db8ff" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="scenarioB" stroke="#a371f7" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="scenarioC" stroke="#3fb950" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-2 flex gap-4 text-xs font-medium">
            <span className="text-cyan">Scenario A</span>
            <span className="text-purple">Scenario B</span>
            <span className="text-success">Scenario C</span>
          </div>
        </Section>
        <Section title="Scenario comparison">
          <table className="w-full text-sm">
            <thead className="text-xs text-muted-foreground"><tr><th className="text-left">Scenario</th><th>Mean</th><th>P5</th><th>P95</th><th>P(loss)</th></tr></thead>
            <tbody>
              {[["Baseline", "+0.4%", "-1.8%", "+2.4%", "31%"], ["Trade war", "-0.9%", "-3.7%", "+0.8%", "78%"], ["Soft landing", "+1.2%", "-0.4%", "+2.9%", "12%"], ["Black swan", "-2.4%", "-7.1%", "-0.2%", "94%"]].map(([n, ...vals]) => (
                <tr key={n} className="border-b border-border/50"><td className="py-2.5 font-medium">{n}</td>{vals.map((v, i) => <td key={i} className="text-center font-mono">{v}</td>)}</tr>
              ))}
            </tbody>
          </table>
        </Section>
      </div>
    </div>
  );
}
