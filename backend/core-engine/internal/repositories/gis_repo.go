package repositories

import (
	"context"
	"github.com/sribash/world-simulation-engine/core-engine/internal/models"
	"gorm.io/gorm"
)

type GisRepository interface {
	CreateMapLayer(ctx context.Context, item *models.MapLayer) error
	GetMapLayerByID(ctx context.Context, id string) (*models.MapLayer, error)
	CreateTopology(ctx context.Context, item *models.Topology) error
	GetTopologyByID(ctx context.Context, id string) (*models.Topology, error)
}

type gisRepository struct {
	db *gorm.DB
}

func NewGisRepository(db *gorm.DB) GisRepository {
	return &gisRepository{db: db}
}

func (r *gisRepository) CreateMapLayer(ctx context.Context, item *models.MapLayer) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *gisRepository) GetMapLayerByID(ctx context.Context, id string) (*models.MapLayer, error) {
	var item models.MapLayer
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}

func (r *gisRepository) CreateTopology(ctx context.Context, item *models.Topology) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *gisRepository) GetTopologyByID(ctx context.Context, id string) (*models.Topology, error) {
	var item models.Topology
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}
