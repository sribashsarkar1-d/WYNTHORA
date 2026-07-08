package repositories

import (
	"context"
	"github.com/sribash/world-simulation-engine/core-engine/internal/models"
	"gorm.io/gorm"
)

type MlopsRepository interface {
	CreateMLModel(ctx context.Context, item *models.MLModel) error
	GetMLModelByID(ctx context.Context, id string) (*models.MLModel, error)
	CreateDataset(ctx context.Context, item *models.Dataset) error
	GetDatasetByID(ctx context.Context, id string) (*models.Dataset, error)
}

type mlopsRepository struct {
	db *gorm.DB
}

func NewMlopsRepository(db *gorm.DB) MlopsRepository {
	return &mlopsRepository{db: db}
}

func (r *mlopsRepository) CreateMLModel(ctx context.Context, item *models.MLModel) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *mlopsRepository) GetMLModelByID(ctx context.Context, id string) (*models.MLModel, error) {
	var item models.MLModel
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}

func (r *mlopsRepository) CreateDataset(ctx context.Context, item *models.Dataset) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *mlopsRepository) GetDatasetByID(ctx context.Context, id string) (*models.Dataset, error) {
	var item models.Dataset
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}
