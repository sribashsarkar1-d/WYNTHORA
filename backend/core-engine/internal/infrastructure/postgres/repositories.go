package postgres

import (
	"context"

	"github.com/google/uuid"
	"github.com/sribash/world-simulation-engine/core-engine/internal/core/domain"
	"github.com/sribash/world-simulation-engine/core-engine/internal/core/ports"
	"gorm.io/gorm"
)

type userRepository struct {
	db *gorm.DB
}

func NewUserRepository(db *gorm.DB) ports.UserRepository {
	return &userRepository{db: db}
}

func (r *userRepository) Create(ctx context.Context, user *domain.User) error {
	return r.db.WithContext(ctx).Create(user).Error
}

func (r *userRepository) GetByID(ctx context.Context, id uuid.UUID) (*domain.User, error) {
	var user domain.User
	if err := r.db.WithContext(ctx).First(&user, id).Error; err != nil {
		return nil, err
	}
	return &user, nil
}

func (r *userRepository) GetByEmail(ctx context.Context, email string) (*domain.User, error) {
	var user domain.User
	if err := r.db.WithContext(ctx).Where("email = ?", email).First(&user).Error; err != nil {
		return nil, err
	}
	return &user, nil
}

func (r *userRepository) GetByOrgID(ctx context.Context, orgID uuid.UUID) ([]*domain.User, error) {
	var users []*domain.User
	if err := r.db.WithContext(ctx).Where("org_id = ?", orgID).Find(&users).Error; err != nil {
		return nil, err
	}
	return users, nil
}

func (r *userRepository) GetAll(ctx context.Context) ([]*domain.User, error) {
	var users []*domain.User
	if err := r.db.WithContext(ctx).Find(&users).Error; err != nil {
		return nil, err
	}
	return users, nil
}

func (r *userRepository) Update(ctx context.Context, user *domain.User) error {
	return r.db.WithContext(ctx).Save(user).Error
}

func (r *userRepository) Delete(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Delete(&domain.User{}, id).Error
}

type orgRepository struct {
	db *gorm.DB
}

func NewOrgRepository(db *gorm.DB) ports.OrgRepository {
	return &orgRepository{db: db}
}

func (r *orgRepository) Create(ctx context.Context, org *domain.Organization) error {
	return r.db.WithContext(ctx).Create(org).Error
}

func (r *orgRepository) GetByID(ctx context.Context, id uuid.UUID) (*domain.Organization, error) {
	var org domain.Organization
	if err := r.db.WithContext(ctx).First(&org, id).Error; err != nil {
		return nil, err
	}
	return &org, nil
}

type roleRepository struct {
	db *gorm.DB
}

func NewRoleRepository(db *gorm.DB) ports.RoleRepository {
	return &roleRepository{db: db}
}

func (r *roleRepository) GetByName(ctx context.Context, name string) (*domain.Role, error) {
	var role domain.Role
	if err := r.db.WithContext(ctx).Where("name = ?", name).First(&role).Error; err != nil {
		return nil, err
	}
	return &role, nil
}

type apiKeyRepository struct {
	db *gorm.DB
}

func NewApiKeyRepository(db *gorm.DB) ports.ApiKeyRepository {
	return &apiKeyRepository{db: db}
}

func (r *apiKeyRepository) Create(ctx context.Context, apiKey *domain.ApiKey) error {
	return r.db.WithContext(ctx).Create(apiKey).Error
}

func (r *apiKeyRepository) GetByUserID(ctx context.Context, userID uuid.UUID) ([]*domain.ApiKey, error) {
	var keys []*domain.ApiKey
	if err := r.db.WithContext(ctx).Where("user_id = ? AND is_revoked = ?", userID, false).Find(&keys).Error; err != nil {
		return nil, err
	}
	return keys, nil
}

func (r *apiKeyRepository) Delete(ctx context.Context, id uuid.UUID) error {
	return r.db.WithContext(ctx).Model(&domain.ApiKey{}).Where("id = ?", id).Update("is_revoked", true).Error
}

type orgInviteRepository struct {
	db *gorm.DB
}

func NewOrgInviteRepository(db *gorm.DB) ports.OrgInviteRepository {
	return &orgInviteRepository{db: db}
}

func (r *orgInviteRepository) Create(ctx context.Context, invite *domain.OrganizationInvite) error {
	return r.db.WithContext(ctx).Create(invite).Error
}

type mfaRepository struct {
	db *gorm.DB
}

func NewMfaRepository(db *gorm.DB) ports.MfaRepository {
	return &mfaRepository{db: db}
}

func (r *mfaRepository) GetByUserID(ctx context.Context, userID uuid.UUID) ([]*domain.UserMfaDevice, error) {
	var devices []*domain.UserMfaDevice
	if err := r.db.WithContext(ctx).Where("user_id = ?", userID).Find(&devices).Error; err != nil {
		return nil, err
	}
	return devices, nil
}
