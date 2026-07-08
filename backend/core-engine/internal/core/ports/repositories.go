package ports

import (
	"context"

	"github.com/google/uuid"
	"github.com/sribash/world-simulation-engine/core-engine/internal/core/domain"
)

type UserRepository interface {
	Create(ctx context.Context, user *domain.User) error
	GetByID(ctx context.Context, id uuid.UUID) (*domain.User, error)
	GetByEmail(ctx context.Context, email string) (*domain.User, error)
	GetByOrgID(ctx context.Context, orgID uuid.UUID) ([]*domain.User, error)
	GetAll(ctx context.Context) ([]*domain.User, error)
	Update(ctx context.Context, user *domain.User) error
	Delete(ctx context.Context, id uuid.UUID) error
}

type OrgRepository interface {
	Create(ctx context.Context, org *domain.Organization) error
	GetByID(ctx context.Context, id uuid.UUID) (*domain.Organization, error)
}

type RoleRepository interface {
	GetByName(ctx context.Context, name string) (*domain.Role, error)
}

type ApiKeyRepository interface {
	Create(ctx context.Context, apiKey *domain.ApiKey) error
	GetByUserID(ctx context.Context, userID uuid.UUID) ([]*domain.ApiKey, error)
	Delete(ctx context.Context, id uuid.UUID) error
}

type OrgInviteRepository interface {
	Create(ctx context.Context, invite *domain.OrganizationInvite) error
}

type MfaRepository interface {
	GetByUserID(ctx context.Context, userID uuid.UUID) ([]*domain.UserMfaDevice, error)
}
