import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/ui-x/Stub";

export const Route = createFileRoute("/organizations")({
  head: () => ({ meta: [{ title: "Organizations — WYNTHORA" }] }),
  component: () => (
    <ModulePage
      eyebrow="Access · Tenancy"
      title="Organization Management"
      description="Manage enterprise customers, government agencies, research institutes and their internal hierarchy."
      sections={[
        { label: "Hierarchy", items: ["Organizations","Departments","Teams","Projects","Workspaces"] },
        { label: "Tenant Classes", items: ["Enterprise Customers","Government Agencies","Research Institutes","Licenses"] },
      ]}
    />
  ),
});
