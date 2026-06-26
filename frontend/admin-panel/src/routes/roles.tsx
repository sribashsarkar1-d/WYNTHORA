import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/ui-x/Stub";

export const Route = createFileRoute("/roles")({
  head: () => ({ meta: [{ title: "Roles & Permissions — WYNTHORA" }] }),
  component: () => (
    <ModulePage
      eyebrow="Access · RBAC"
      title="Roles & Permission Management"
      description="Fine-grained RBAC, role cloning, and policy management across all tenant classes."
      sections={[
        { label: "Role Catalog", items: ["System Roles","Enterprise Roles","Government Roles","Research Roles","Create Role","Clone Role","Delete Role"] },
        { label: "Authorization", items: ["RBAC","Permission Matrix","Fine Grained Permissions","Policy Management","Attribute-Based Rules"] },
      ]}
    />
  ),
});
