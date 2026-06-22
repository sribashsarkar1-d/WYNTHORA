import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/module-page";
export const Route = createFileRoute("/app/trade")({ component: () => <ModulePage kicker="Supply chain" title="Trade & Logistics" color="var(--color-success)"
  kpis={[
    { label: "Global trade vol.", value: "$32.1T", delta: "+3.1%" },
    { label: "Container index", value: "1,847", delta: "+218" },
    { label: "Choke point risk", value: "Elevated", delta: "+1" },
    { label: "Tariff coverage", value: "11.3%", delta: "+0.4%" },
  ]} /> });
