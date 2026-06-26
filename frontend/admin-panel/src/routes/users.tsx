import { createFileRoute } from "@tanstack/react-router";
import { ModulePage } from "@/components/ui-x/Stub";

export const Route = createFileRoute("/users")({
  head: () => ({ meta: [{ title: "User Management — WYNTHORA" }] }),
  component: () => (
    <ModulePage
      eyebrow="Access · Users"
      title="User Management"
      description="Provision, govern, and audit every identity across enterprise, government, and research tenants."
      sections={[
        { label: "Lifecycle", items: ["Create User","Edit User","Suspend User","Activate User","Delete User","Reset Password","Force Logout"] },
        { label: "Assignment", items: ["Assign Organization","Assign Role","Assign Subscription","Enterprise Assignment"] },
        { label: "Telemetry", items: ["User Timeline","Login History","Devices","Sessions","API Usage","Simulation History","Storage Usage"] },
        { label: "Bulk Operations", items: ["Bulk Import","Bulk Export","Advanced Filters","Saved Searches"] },
      ]}
    />
  ),
});
