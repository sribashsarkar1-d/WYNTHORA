package services

import (
	"context"
	"github.com/sribash/world-simulation-engine/core-engine/internal/models"
	"github.com/sribash/world-simulation-engine/core-engine/internal/repositories"
)

type GisService interface {
	CreateMapLayer(ctx context.Context, item *models.MapLayer) error
	GetMapLayerByID(ctx context.Context, id string) (*models.MapLayer, error)
	CreateTopology(ctx context.Context, item *models.Topology) error
	GetTopologyByID(ctx context.Context, id string) (*models.Topology, error)
}

type gisService struct {
	repo repositories.GisRepository
}

func NewGisService(repo repositories.GisRepository) GisService {
	return &gisService{repo: repo}
}

func (s *gisService) CreateMapLayer(ctx context.Context, item *models.MapLayer) error {
	return s.repo.CreateMapLayer(ctx, item)
}

func (s *gisService) GetMapLayerByID(ctx context.Context, id string) (*models.MapLayer, error) {
	return s.repo.GetMapLayerByID(ctx, id)
}

func (s *gisService) CreateTopology(ctx context.Context, item *models.Topology) error {
	return s.repo.CreateTopology(ctx, item)
}

func (s *gisService) GetTopologyByID(ctx context.Context, id string) (*models.Topology, error) {
	return s.repo.GetTopologyByID(ctx, id)
}
