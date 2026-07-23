import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { Field } from "./_auth.login";
import { Building2, Mail, User, Loader2 } from "lucide-react";
import { useState } from "react";

export const Route = createFileRoute("/_auth/register")({ component: Register });

function Register() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    // Mock API call
    setTimeout(() => {
      setIsLoading(false);
      navigate({ to: "/mfa" });
    }, 1000);
  };

  return (
    <div>
      <h1 className="font-display text-3xl font-bold">Request access</h1>
      <p className="mt-2 text-sm text-muted-foreground">All accounts are vetted by our compliance team within 24 hours.</p>
      <form onSubmit={handleSubmit} className="mt-8 space-y-4">
        <div className="grid gap-4 sm:grid-cols-2">
          <Field icon={<User className="h-4 w-4" />} label="Full name" placeholder="Dr. Jane Chen" required />
          <Field icon={<Building2 className="h-4 w-4" />} label="Institution" placeholder="Sovereign Wealth Co." required />
        </div>
        <Field icon={<Mail className="h-4 w-4" />} label="Work email" type="email" placeholder="jane@institution.gov" required />
        <Field label="Password" type="password" placeholder="At least 14 characters" required />
        <label className="flex items-start gap-2 text-xs text-muted-foreground"><input type="checkbox" className="mt-0.5 accent-cyan" required /> I represent a qualified institutional investor, research body, or sovereign entity, and agree to the WYNTHORA terms.</label>
        <button type="submit" disabled={isLoading} className="flex w-full items-center justify-center gap-2 rounded-lg bg-gradient-to-r from-cyan to-purple py-2.5 text-sm font-semibold text-background disabled:opacity-70 transition">
          {isLoading && <Loader2 className="h-4 w-4 animate-spin" />}
          Submit request
        </button>
      </form>
      <p className="mt-8 text-center text-xs text-muted-foreground">Already approved? <Link to="/login" className="text-cyan hover:underline">Sign in</Link></p>
    </div>
  );
}
