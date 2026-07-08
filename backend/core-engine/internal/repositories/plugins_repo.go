package repositories

import (
	"context"
	"github.com/sribash/world-simulation-engine/core-engine/internal/models"
	"gorm.io/gorm"
)

type PluginsRepository interface {
	CreatePlugin(ctx context.Context, item *models.Plugin) error
	GetPluginByID(ctx context.Context, id string) (*models.Plugin, error)
	CreatePluginReview(ctx context.Context, item *models.PluginReview) error
	GetPluginReviewByID(ctx context.Context, id string) (*models.PluginReview, error)
}

type pluginsRepository struct {
	db *gorm.DB
}

func NewPluginsRepository(db *gorm.DB) PluginsRepository {
	return &pluginsRepository{db: db}
}

func (r *pluginsRepository) CreatePlugin(ctx context.Context, item *models.Plugin) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *pluginsRepository) GetPluginByID(ctx context.Context, id string) (*models.Plugin, error) {
	var item models.Plugin
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}

func (r *pluginsRepository) CreatePluginReview(ctx context.Context, item *models.PluginReview) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *pluginsRepository) GetPluginReviewByID(ctx context.Context, id string) (*models.PluginReview, error) {
	var item models.PluginReview
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}
