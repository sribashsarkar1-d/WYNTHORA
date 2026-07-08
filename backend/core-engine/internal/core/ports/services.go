package ports

import (
	"context"

	"github.com/google/uuid"
	"github.com/sribash/world-simulation-engine/core-engine/internal/core/domain"
)

type AuthService interface {
	Login(ctx context.Context, email, password string) (string, error)
	Register(ctx context.Context, email, password, orgName string) (*domain.User, error)
	VerifyMFA(ctx context.Context, userID uuid.UUID, code string) (string, error)
	GenerateApiKey(ctx context.Context, userID uuid.UUID, name string) (string, error)
	GetApiKeys(ctx context.Context, userID uuid.UUID) ([]*domain.ApiKey, error)
	RevokeApiKey(ctx context.Context, keyID uuid.UUID) error
	GetAllUsers(ctx context.Context) ([]*domain.User, error)
}

type OrgService interface {
	GetMembers(ctx context.Context, orgID uuid.UUID) ([]*domain.User, error)
	CreateInvite(ctx context.Context, orgID uuid.UUID, email, roleName string) (*domain.OrganizationInvite, error)
	UpdateUserRole(ctx context.Context, orgID, userID uuid.UUID, roleName string) error
}

type UserService interface {
	GetProfile(ctx context.Context, userID uuid.UUID) (*domain.User, error)
	DeleteUser(ctx context.Context, userID uuid.UUID) error
}
