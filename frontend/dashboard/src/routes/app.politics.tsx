import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/module-page";
export const Route = createFileRoute("/app/politics")({ component: () => <ModulePage kicker="Geopolitical reasoning" title="Political Intelligence" color="var(--color-purple)"
  kpis={[
    { label: "Stability index", value: "62 / 100", delta: "-1.4" },
    { label: "Elections Q", value: "23", delta: "+5" },
    { label: "Active conflicts", value: "14", delta: "+2" },
    { label: "Coup risk (>0.3)", value: "7 states", delta: "+1" },
  ]} /> });
