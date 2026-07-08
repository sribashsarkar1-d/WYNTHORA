package services

import (
	"context"
	"github.com/sribash/world-simulation-engine/core-engine/internal/models"
	"github.com/sribash/world-simulation-engine/core-engine/internal/repositories"
)

type AuthService interface {
	CreateUser(ctx context.Context, item *models.User) error
	GetUserByID(ctx context.Context, id string) (*models.User, error)
	CreateOrg(ctx context.Context, item *models.Org) error
	GetOrgByID(ctx context.Context, id string) (*models.Org, error)
	CreateAPIKey(ctx context.Context, item *models.APIKey) error
	GetAPIKeyByID(ctx context.Context, id string) (*models.APIKey, error)
}

type authService struct {
	repo repositories.AuthRepository
}

func NewAuthService(repo repositories.AuthRepository) AuthService {
	return &authService{repo: repo}
}

func (s *authService) CreateUser(ctx context.Context, item *models.User) error {
	return s.repo.CreateUser(ctx, item)
}

func (s *authService) GetUserByID(ctx context.Context, id string) (*models.User, error) {
	return s.repo.GetUserByID(ctx, id)
}

func (s *authService) CreateOrg(ctx context.Context, item *models.Org) error {
	return s.repo.CreateOrg(ctx, item)
}

func (s *authService) GetOrgByID(ctx context.Context, id string) (*models.Org, error) {
	return s.repo.GetOrgByID(ctx, id)
}

func (s *authService) CreateAPIKey(ctx context.Context, item *models.APIKey) error {
	return s.repo.CreateAPIKey(ctx, item)
}

func (s *authService) GetAPIKeyByID(ctx context.Context, id string) (*models.APIKey, error) {
	return s.repo.GetAPIKeyByID(ctx, id)
}
