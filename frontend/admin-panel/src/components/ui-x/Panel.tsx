import type { ReactNode } from "react";

export function Panel({
  title, subtitle, action, children, className = "", padded = true, accent = false,
}: {
  title?: ReactNode;
  subtitle?: ReactNode;
  action?: ReactNode;
  children: ReactNode;
  className?: string;
  padded?: boolean;
  accent?: boolean;
}) {
  return (
    <section className={`relative rounded-xl glass ${accent ? "glow-cyan" : ""} ${className}`}>
      {accent && (
        <div className="pointer-events-none absolute inset-x-0 -top-px h-px bg-gradient-to-r from-transparent via-primary to-transparent" />
      )}
      {(title || action) && (
        <header className="flex items-center justify-between gap-4 border-b border-border/60 px-4 py-3">
          <div className="min-w-0">
            {title && <h3 className="font-display text-sm font-semibold tracking-wide">{title}</h3>}
            {subtitle && <p className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground mt-0.5">{subtitle}</p>}
          </div>
          {action && <div className="shrink-0">{action}</div>}
        </header>
      )}
      <div className={padded ? "p-4" : ""}>{children}</div>
    </section>
  );
}

export function PageHeader({
  eyebrow, title, description, actions,
}: { eyebrow?: string; title: string; description?: string; actions?: ReactNode }) {
  return (
    <div className="mb-6 grid grid-cols-[minmax(0,1fr)_auto] items-end gap-4">
      <div className="min-w-0">
        {eyebrow && (
          <div className="font-mono text-[10px] uppercase tracking-[0.2em] text-primary mb-2">{eyebrow}</div>
        )}
        <h1 className="font-display text-2xl sm:text-3xl font-bold tracking-tight">{title}</h1>
        {description && <p className="mt-1.5 text-sm text-muted-foreground max-w-2xl">{description}</p>}
      </div>
      {actions && <div className="flex items-center gap-2">{actions}</div>}
    </div>
  );
}

export function Btn({
  children, variant = "default", size = "md", className = "", ...rest
}: React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: "default" | "primary" | "ghost" | "danger"; size?: "sm" | "md" }) {
  const variants = {
    default: "glass hover:bg-surface-2 text-foreground",
    primary: "bg-[var(--gradient-aurora)] text-primary-foreground hover:glow-cyan font-semibold",
    ghost: "text-muted-foreground hover:bg-surface-2 hover:text-foreground",
    danger: "bg-destructive/15 text-destructive hover:bg-destructive/25 border border-destructive/30",
  } as const;
  const sizes = { sm: "h-7 px-2.5 text-xs", md: "h-9 px-3.5 text-sm" } as const;
  return (
    <button
      {...rest}
      className={`inline-flex items-center justify-center gap-1.5 rounded-md transition-all ${variants[variant]} ${sizes[size]} ${className}`}
    >
      {children}
    </button>
  );
}

export function Pill({ tone = "muted", children }: { tone?: "muted" | "primary" | "success" | "warning" | "danger" | "secondary"; children: ReactNode }) {
  const tones = {
    muted: "bg-muted text-muted-foreground border-border",
    primary: "bg-primary/15 text-primary border-primary/30",
    success: "bg-success/15 text-success border-success/30",
    warning: "bg-warning/15 text-warning border-warning/30",
    danger: "bg-destructive/15 text-destructive border-destructive/30",
    secondary: "bg-secondary/15 text-secondary border-secondary/30",
  } as const;
  return (
    <span className={`inline-flex items-center gap-1 rounded-sm border px-1.5 py-0.5 font-mono text-[10px] font-semibold uppercase tracking-wider ${tones[tone]}`}>
      {children}
    </span>
  );
}
