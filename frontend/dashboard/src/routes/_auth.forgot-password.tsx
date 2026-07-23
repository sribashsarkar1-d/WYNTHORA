import { createFileRoute, Link } from "@tanstack/react-router";
import { Field } from "./_auth.login";
import { Mail, Loader2, CheckCircle2 } from "lucide-react";
import { useState } from "react";

export const Route = createFileRoute("/_auth/forgot-password")({ component: Forgot });

function Forgot() {
  const [isLoading, setIsLoading] = useState(false);
  const [isSent, setIsSent] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    // Mock API call
    setTimeout(() => {
      setIsLoading(false);
      setIsSent(true);
    }, 1000);
  };

  return (
    <div>
      <h1 className="font-display text-3xl font-bold">Reset credentials</h1>
      <p className="mt-2 text-sm text-muted-foreground">We will send a hardware-key-bound recovery link to your registered address.</p>
      
      {isSent ? (
        <div className="mt-8 rounded-lg border border-success/30 bg-success/10 p-4 text-sm text-success flex items-center gap-3">
          <CheckCircle2 className="h-5 w-5" />
          Recovery link sent successfully! Please check your email.
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="mt-8 space-y-4">
          <Field icon={<Mail className="h-4 w-4" />} label="Work email" type="email" placeholder="analyst@institution.gov" required />
          <button type="submit" disabled={isLoading} className="flex w-full items-center justify-center gap-2 rounded-lg bg-gradient-to-r from-cyan to-purple py-2.5 text-sm font-semibold text-background disabled:opacity-70 transition">
            {isLoading && <Loader2 className="h-4 w-4 animate-spin" />}
            Send recovery link
          </button>
        </form>
      )}
      <p className="mt-8 text-center text-xs text-muted-foreground"><Link to="/login" className="text-cyan hover:underline">← Back to sign in</Link></p>
    </div>
  );
}
