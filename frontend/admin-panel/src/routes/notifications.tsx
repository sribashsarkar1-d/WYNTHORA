import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/ui-x/Stub";

export const Route = createFileRoute("/notifications")({
  head: () => ({ meta: [{ title: "Notifications — WYNTHORA" }] }),
  component: () => (
    <ModulePage
      eyebrow="Operations · Notify"
      title="Notification Center"
      description="Cross-channel alerting and rules engine."
      sections={[
        { label: "Channels", items: ["Email","SMS","Push","Slack","Teams","Discord","Webhook"] },
        { label: "Rules", items: ["Alert Rules","Routing","Escalation","Quiet Hours"] },
      ]}
    />
  ),
});
