package repositories

import (
	"context"
	"github.com/sribash/world-simulation-engine/core-engine/internal/models"
	"gorm.io/gorm"
)

type MarketRepository interface {
	CreateEconomicIndicator(ctx context.Context, item *models.EconomicIndicator) error
	GetEconomicIndicatorByID(ctx context.Context, id string) (*models.EconomicIndicator, error)
	CreateClimateSensor(ctx context.Context, item *models.ClimateSensor) error
	GetClimateSensorByID(ctx context.Context, id string) (*models.ClimateSensor, error)
	CreateDataSource(ctx context.Context, item *models.DataSource) error
	GetDataSourceByID(ctx context.Context, id string) (*models.DataSource, error)
}

type marketRepository struct {
	db *gorm.DB
}

func NewMarketRepository(db *gorm.DB) MarketRepository {
	return &marketRepository{db: db}
}

func (r *marketRepository) CreateEconomicIndicator(ctx context.Context, item *models.EconomicIndicator) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *marketRepository) GetEconomicIndicatorByID(ctx context.Context, id string) (*models.EconomicIndicator, error) {
	var item models.EconomicIndicator
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}

func (r *marketRepository) CreateClimateSensor(ctx context.Context, item *models.ClimateSensor) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *marketRepository) GetClimateSensorByID(ctx context.Context, id string) (*models.ClimateSensor, error) {
	var item models.ClimateSensor
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}

func (r *marketRepository) CreateDataSource(ctx context.Context, item *models.DataSource) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *marketRepository) GetDataSourceByID(ctx context.Context, id string) (*models.DataSource, error) {
	var item models.DataSource
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}
