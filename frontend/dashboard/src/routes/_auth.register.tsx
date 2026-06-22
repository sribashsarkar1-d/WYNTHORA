import { createFileRoute, Link } from "@tanstack/react-router";
import { Field } from "./_auth.login";
import { Building2, Mail, User } from "lucide-react";

export const Route = createFileRoute("/_auth/register")({ component: Register });

function Register() {
  return (
    <div>
      <h1 className="font-display text-3xl font-bold">Request access</h1>
      <p className="mt-2 text-sm text-muted-foreground">All accounts are vetted by our compliance team within 24 hours.</p>
      <form className="mt-8 space-y-4">
        <div className="grid gap-4 sm:grid-cols-2">
          <Field icon={<User className="h-4 w-4" />} label="Full name" placeholder="Dr. Jane Chen" />
          <Field icon={<Building2 className="h-4 w-4" />} label="Institution" placeholder="Sovereign Wealth Co." />
        </div>
        <Field icon={<Mail className="h-4 w-4" />} label="Work email" type="email" placeholder="jane@institution.gov" />
        <Field label="Password" type="password" placeholder="At least 14 characters" />
        <label className="flex items-start gap-2 text-xs text-muted-foreground"><input type="checkbox" className="mt-0.5 accent-cyan" /> I represent a qualified institutional investor, research body, or sovereign entity, and agree to the WYNTHORA terms.</label>
        <Link to="/mfa" className="block w-full rounded-lg bg-gradient-to-r from-cyan to-purple py-2.5 text-center text-sm font-semibold text-background">Submit request</Link>
      </form>
      <p className="mt-8 text-center text-xs text-muted-foreground">Already approved? <Link to="/login" className="text-cyan hover:underline">Sign in</Link></p>
    </div>
  );
}
