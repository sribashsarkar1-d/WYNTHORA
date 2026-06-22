import { createFileRoute, Link } from "@tanstack/react-router";
import { Field } from "./_auth.login";
import { Mail } from "lucide-react";
export const Route = createFileRoute("/_auth/forgot-password")({ component: Forgot });
function Forgot() {
  return (
    <div>
      <h1 className="font-display text-3xl font-bold">Reset credentials</h1>
      <p className="mt-2 text-sm text-muted-foreground">We will send a hardware-key-bound recovery link to your registered address.</p>
      <form className="mt-8 space-y-4">
        <Field icon={<Mail className="h-4 w-4" />} label="Work email" type="email" placeholder="analyst@institution.gov" />
        <button className="w-full rounded-lg bg-gradient-to-r from-cyan to-purple py-2.5 text-sm font-semibold text-background">Send recovery link</button>
      </form>
      <p className="mt-8 text-center text-xs text-muted-foreground"><Link to="/login" className="text-cyan hover:underline">← Back to sign in</Link></p>
    </div>
  );
}
