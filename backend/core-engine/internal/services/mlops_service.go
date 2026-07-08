package services

import (
	"context"
	"github.com/sribash/world-simulation-engine/core-engine/internal/models"
	"github.com/sribash/world-simulation-engine/core-engine/internal/repositories"
)

type MlopsService interface {
	CreateMLModel(ctx context.Context, item *models.MLModel) error
	GetMLModelByID(ctx context.Context, id string) (*models.MLModel, error)
	CreateDataset(ctx context.Context, item *models.Dataset) error
	GetDatasetByID(ctx context.Context, id string) (*models.Dataset, error)
}

type mlopsService struct {
	repo repositories.MlopsRepository
}

func NewMlopsService(repo repositories.MlopsRepository) MlopsService {
	return &mlopsService{repo: repo}
}

func (s *mlopsService) CreateMLModel(ctx context.Context, item *models.MLModel) error {
	return s.repo.CreateMLModel(ctx, item)
}

func (s *mlopsService) GetMLModelByID(ctx context.Context, id string) (*models.MLModel, error) {
	return s.repo.GetMLModelByID(ctx, id)
}

func (s *mlopsService) CreateDataset(ctx context.Context, item *models.Dataset) error {
	return s.repo.CreateDataset(ctx, item)
}

func (s *mlopsService) GetDatasetByID(ctx context.Context, id string) (*models.Dataset, error) {
	return s.repo.GetDatasetByID(ctx, id)
}
