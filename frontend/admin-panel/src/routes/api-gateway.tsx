import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/ui-x/Stub";

export const Route = createFileRoute("/api-gateway")({
  head: () => ({ meta: [{ title: "API Gateway — WYNTHORA" }] }),
  component: () => (
    <ModulePage
      eyebrow="Infrastructure · Gateway"
      title="API Gateway Management"
      description="Public/private API surface, keys, quotas, and observability."
      sections={[
        { label: "Surface", items: ["API Gateway","API Keys","Authentication","Rate Limiting"] },
        { label: "Observability", items: ["Logs","Usage Analytics","Error Monitoring","Latency Histograms"] },
      ]}
    />
  ),
});
