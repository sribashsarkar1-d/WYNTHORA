CREATE TABLE public.organization_invites (
    id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    org_id uuid NOT NULL,
    email character varying(255) NOT NULL,
    token character varying(255) NOT NULL,
    role_id uuid,
    expires_at timestamp with time zone NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT organization_invites_pkey PRIMARY KEY (id),
    CONSTRAINT fk_organization_invites_org FOREIGN KEY (org_id) REFERENCES public.organizations (id) ON DELETE CASCADE,
    CONSTRAINT fk_organization_invites_role FOREIGN KEY (role_id) REFERENCES public.roles (id) ON DELETE SET NULL
);

ALTER TABLE public.organization_invites OWNER TO postgres;

CREATE UNIQUE INDEX idx_org_invites_token ON public.organization_invites (token);
