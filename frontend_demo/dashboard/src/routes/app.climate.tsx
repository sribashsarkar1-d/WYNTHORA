import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/module-page";
export const Route = createFileRoute("/app/climate")({ component: () => <ModulePage kicker="Earth systems" title="Climate Simulation" color="var(--color-warning)"
  kpis={[
    { label: "Global ΔT", value: "+1.34°C", delta: "+0.08" },
    { label: "CO₂", value: "424 ppm", delta: "+2.3" },
    { label: "Flood risk index", value: "6.7", delta: "+0.4" },
    { label: "Drought severity", value: "3.2", delta: "-0.1" },
  ]} /> });
