import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/ui-x/Stub";

export const Route = createFileRoute("/settings")({
  head: () => ({ meta: [{ title: "Settings — WYNTHORA" }] }),
  component: () => (
    <ModulePage
      eyebrow="Operations · Settings"
      title="Settings"
      description="Platform configuration, branding, and feature governance."
      sections={[
        { label: "General", items: ["General","Theme","Languages","Time Zones","Branding"] },
        { label: "Infrastructure", items: ["SMTP","Storage","Backup","API Configuration","AI Configuration","Feature Flags"] },
      ]}
    />
  ),
});
