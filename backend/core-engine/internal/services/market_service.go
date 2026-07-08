package services

import (
	"context"
	"github.com/sribash/world-simulation-engine/core-engine/internal/models"
	"github.com/sribash/world-simulation-engine/core-engine/internal/repositories"
)

type MarketService interface {
	CreateEconomicIndicator(ctx context.Context, item *models.EconomicIndicator) error
	GetEconomicIndicatorByID(ctx context.Context, id string) (*models.EconomicIndicator, error)
	CreateClimateSensor(ctx context.Context, item *models.ClimateSensor) error
	GetClimateSensorByID(ctx context.Context, id string) (*models.ClimateSensor, error)
	CreateDataSource(ctx context.Context, item *models.DataSource) error
	GetDataSourceByID(ctx context.Context, id string) (*models.DataSource, error)
}

type marketService struct {
	repo repositories.MarketRepository
}

func NewMarketService(repo repositories.MarketRepository) MarketService {
	return &marketService{repo: repo}
}

func (s *marketService) CreateEconomicIndicator(ctx context.Context, item *models.EconomicIndicator) error {
	return s.repo.CreateEconomicIndicator(ctx, item)
}

func (s *marketService) GetEconomicIndicatorByID(ctx context.Context, id string) (*models.EconomicIndicator, error) {
	return s.repo.GetEconomicIndicatorByID(ctx, id)
}

func (s *marketService) CreateClimateSensor(ctx context.Context, item *models.ClimateSensor) error {
	return s.repo.CreateClimateSensor(ctx, item)
}

func (s *marketService) GetClimateSensorByID(ctx context.Context, id string) (*models.ClimateSensor, error) {
	return s.repo.GetClimateSensorByID(ctx, id)
}

func (s *marketService) CreateDataSource(ctx context.Context, item *models.DataSource) error {
	return s.repo.CreateDataSource(ctx, item)
}

func (s *marketService) GetDataSourceByID(ctx context.Context, id string) (*models.DataSource, error) {
	return s.repo.GetDataSourceByID(ctx, id)
}
