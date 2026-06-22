import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/module-page";
export const Route = createFileRoute("/app/economy")({ component: () => <ModulePage kicker="Macro intelligence" title="Economy" color="var(--color-cyan)"
  kpis={[
    { label: "Global GDP 2025", value: "$108.4T", delta: "+2.4%" },
    { label: "CPI (G7 avg)", value: "2.7%", delta: "-0.3%" },
    { label: "Unemployment (OECD)", value: "5.1%", delta: "+0.1%" },
    { label: "M2 growth", value: "4.8%", delta: "+0.6%" },
  ]} /> });
