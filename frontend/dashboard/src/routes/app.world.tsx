import { createFileRoute } from "@tanstack/react-router";
import { Section, Badge } from "@/components/wynthora";
import { GlobeEngineWrapper } from "@/components/GlobeEngineWrapper";
import { engineEvents, EngineEvent } from "@/engine/events/EventBus";

export const Route = createFileRoute("/app/world")({ component: World });

function World() {

  // Example of Decoupled UI communicating with the Rendering Engine via Event Bus
  const flyToGermany = () => {
    engineEvents.emit(EngineEvent.CAMERA_FLY_TO, { lat: 51.1657, lng: 10.4515, alt: 3000000 });
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-widest text-muted-foreground">Interactive · Real-time</p>
          <h1 className="font-display text-3xl font-bold">World Map (Enterprise Engine)</h1>
        </div>
        <div className="glass flex gap-1 rounded-lg border border-border p-1 text-xs">
          {["Economy", "Climate", "Trade routes", "Conflicts"].map((l, i) => (
            <button key={l} className={`rounded-md px-3 py-1.5 ${i === 0 ? "bg-cyan/20 text-cyan" : "text-muted-foreground hover:bg-white/5 transition-colors"}`}>{l}</button>
          ))}
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-[1fr_320px]">
        <div className="glass rounded-xl p-0 overflow-hidden relative min-h-[500px] flex">
          <GlobeEngineWrapper />
          <div className="absolute top-4 left-4 pointer-events-none z-10">
            <Badge tone="cyan">Rendering Engine: {import.meta.env.VITE_ACTIVE_GLOBE_ENGINE || 'threejs'}</Badge>
          </div>
        </div>
        <div className="space-y-4">
          <Section title="Selected: Germany">
            <dl className="space-y-2 text-sm">
              {[["GDP", "$4.5T"], ["Pop.", "84.5M"], ["Risk", "4.1 / 10"], ["Climate", "+1.7°C"], ["Trade balance", "+€213B"]].map(([k, v]) => (
                <div key={k} className="flex justify-between border-b border-border/50 py-2 text-xs"><dt className="text-muted-foreground">{k}</dt><dd className="font-mono">{v}</dd></div>
              ))}
            </dl>
            <div className="mt-4 flex gap-2">
              <Badge tone="success">stable</Badge> 
              <Badge tone="warning">energy-exposed</Badge>
            </div>
            <button onClick={flyToGermany} className="mt-4 w-full bg-cyan text-black text-xs font-bold py-2 rounded-lg hover:bg-cyan/90 transition-colors">
              Fly To Location
            </button>
          </Section>
          <Section title="Layers">
            <ul className="space-y-2 text-xs">
              {["Economic indicators", "Climate models", "Trade routes", "Conflict zones", "Migration", "Energy grid"].map((l, i) => (
                <li key={l} className="flex items-center justify-between"><label className="flex items-center gap-2 cursor-pointer">
                  <input 
                    type="checkbox" 
                    defaultChecked={i < 3} 
                    className="accent-cyan" 
                    onChange={(e) => engineEvents.emit(EngineEvent.LAYER_TOGGLE, { id: l, visible: e.target.checked })}
                  />
                  {l}
                </label><span className="text-muted-foreground font-mono">{Math.round(Math.random() * 100)}</span></li>
              ))}
            </ul>
          </Section>
        </div>
      </div>
    </div>
  );
}
