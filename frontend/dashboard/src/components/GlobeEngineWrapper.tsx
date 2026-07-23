import { useEffect, useRef, useState } from 'react';
import { GlobeEngineFactory } from '../engine/core/GlobeEngineFactory';
import { IGlobeEngine } from '../engine/core/IGlobeEngine';

// Environment variable feature flag fallback
const activeEngine = import.meta.env.VITE_ACTIVE_GLOBE_ENGINE || 'threejs';

export function GlobeEngineWrapper({ className }: { className?: string }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const engineRef = useRef<IGlobeEngine | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    let isMounted = true;

    // Async initialize the engine
    const initEngine = async () => {
      try {
        console.log(`[GlobeEngineWrapper] Loading engine: ${activeEngine}`);
        
        // Prevent double init in StrictMode
        if (engineRef.current) {
           engineRef.current.destroy();
        }

        const engine = await GlobeEngineFactory.createEngine(activeEngine as any);
        if (!isMounted) return;

        engineRef.current = engine;
        engine.initialize(containerRef.current!);
      } catch (err: any) {
        console.error('[GlobeEngineWrapper] Failed to initialize engine', err);
        setError(err.message);
      }
    };

    initEngine();

    return () => {
      isMounted = false;
      if (engineRef.current) {
        engineRef.current.destroy();
        engineRef.current = null;
      }
    };
  }, []);

  if (error) {
    return <div className="w-full h-full flex items-center justify-center text-red-500">Engine Error: {error}</div>;
  }

  // The engine will mount into this DOM element directly
  return (
    <div ref={containerRef} className={`w-full h-full flex-1 bg-[#04060a] overflow-hidden ${className || 'min-h-[500px]'}`} />
  );
}
