package repositories

import (
	"context"
	"github.com/sribash/world-simulation-engine/core-engine/internal/models"
	"gorm.io/gorm"
)

type SimulationRepository interface {
	CreateSimulation(ctx context.Context, item *models.Simulation) error
	GetSimulationByID(ctx context.Context, id string) (*models.Simulation, error)
	CreateScenario(ctx context.Context, item *models.Scenario) error
	GetScenarioByID(ctx context.Context, id string) (*models.Scenario, error)
	CreateSimulationLog(ctx context.Context, item *models.SimulationLog) error
	GetSimulationLogByID(ctx context.Context, id string) (*models.SimulationLog, error)
	CreateSimulationMetric(ctx context.Context, item *models.SimulationMetric) error
	GetSimulationMetricByID(ctx context.Context, id string) (*models.SimulationMetric, error)
	CreateSimulationTemplate(ctx context.Context, item *models.SimulationTemplate) error
	GetSimulationTemplateByID(ctx context.Context, id string) (*models.SimulationTemplate, error)
}

type simulationRepository struct {
	db *gorm.DB
}

func NewSimulationRepository(db *gorm.DB) SimulationRepository {
	return &simulationRepository{db: db}
}

func (r *simulationRepository) CreateSimulation(ctx context.Context, item *models.Simulation) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *simulationRepository) GetSimulationByID(ctx context.Context, id string) (*models.Simulation, error) {
	var item models.Simulation
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}

func (r *simulationRepository) CreateScenario(ctx context.Context, item *models.Scenario) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *simulationRepository) GetScenarioByID(ctx context.Context, id string) (*models.Scenario, error) {
	var item models.Scenario
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}

func (r *simulationRepository) CreateSimulationLog(ctx context.Context, item *models.SimulationLog) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *simulationRepository) GetSimulationLogByID(ctx context.Context, id string) (*models.SimulationLog, error) {
	var item models.SimulationLog
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}

func (r *simulationRepository) CreateSimulationMetric(ctx context.Context, item *models.SimulationMetric) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *simulationRepository) GetSimulationMetricByID(ctx context.Context, id string) (*models.SimulationMetric, error) {
	var item models.SimulationMetric
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}

func (r *simulationRepository) CreateSimulationTemplate(ctx context.Context, item *models.SimulationTemplate) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *simulationRepository) GetSimulationTemplateByID(ctx context.Context, id string) (*models.SimulationTemplate, error) {
	var item models.SimulationTemplate
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}
