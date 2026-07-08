package services

import (
	"context"
	"github.com/sribash/world-simulation-engine/core-engine/internal/models"
	"github.com/sribash/world-simulation-engine/core-engine/internal/repositories"
)

type PluginsService interface {
	CreatePlugin(ctx context.Context, item *models.Plugin) error
	GetPluginByID(ctx context.Context, id string) (*models.Plugin, error)
	CreatePluginReview(ctx context.Context, item *models.PluginReview) error
	GetPluginReviewByID(ctx context.Context, id string) (*models.PluginReview, error)
}

type pluginsService struct {
	repo repositories.PluginsRepository
}

func NewPluginsService(repo repositories.PluginsRepository) PluginsService {
	return &pluginsService{repo: repo}
}

func (s *pluginsService) CreatePlugin(ctx context.Context, item *models.Plugin) error {
	return s.repo.CreatePlugin(ctx, item)
}

func (s *pluginsService) GetPluginByID(ctx context.Context, id string) (*models.Plugin, error) {
	return s.repo.GetPluginByID(ctx, id)
}

func (s *pluginsService) CreatePluginReview(ctx context.Context, item *models.PluginReview) error {
	return s.repo.CreatePluginReview(ctx, item)
}

func (s *pluginsService) GetPluginReviewByID(ctx context.Context, id string) (*models.PluginReview, error) {
	return s.repo.GetPluginReviewByID(ctx, id)
}
