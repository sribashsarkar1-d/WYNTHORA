package repositories

import (
	"context"
	"github.com/sribash/world-simulation-engine/core-engine/internal/models"
	"gorm.io/gorm"
)

type AuthRepository interface {
	CreateUser(ctx context.Context, item *models.User) error
	GetUserByID(ctx context.Context, id string) (*models.User, error)
	CreateOrg(ctx context.Context, item *models.Org) error
	GetOrgByID(ctx context.Context, id string) (*models.Org, error)
	CreateAPIKey(ctx context.Context, item *models.APIKey) error
	GetAPIKeyByID(ctx context.Context, id string) (*models.APIKey, error)
}

type authRepository struct {
	db *gorm.DB
}

func NewAuthRepository(db *gorm.DB) AuthRepository {
	return &authRepository{db: db}
}

func (r *authRepository) CreateUser(ctx context.Context, item *models.User) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *authRepository) GetUserByID(ctx context.Context, id string) (*models.User, error) {
	var item models.User
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}

func (r *authRepository) CreateOrg(ctx context.Context, item *models.Org) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *authRepository) GetOrgByID(ctx context.Context, id string) (*models.Org, error) {
	var item models.Org
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}

func (r *authRepository) CreateAPIKey(ctx context.Context, item *models.APIKey) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *authRepository) GetAPIKeyByID(ctx context.Context, id string) (*models.APIKey, error) {
	var item models.APIKey
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}
