package services

import (
	"context"
	"github.com/sribash/world-simulation-engine/core-engine/internal/models"
	"github.com/sribash/world-simulation-engine/core-engine/internal/repositories"
)

type SimulationService interface {
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

type simulationService struct {
	repo repositories.SimulationRepository
}

func NewSimulationService(repo repositories.SimulationRepository) SimulationService {
	return &simulationService{repo: repo}
}

func (s *simulationService) CreateSimulation(ctx context.Context, item *models.Simulation) error {
	return s.repo.CreateSimulation(ctx, item)
}

func (s *simulationService) GetSimulationByID(ctx context.Context, id string) (*models.Simulation, error) {
	return s.repo.GetSimulationByID(ctx, id)
}

func (s *simulationService) CreateScenario(ctx context.Context, item *models.Scenario) error {
	return s.repo.CreateScenario(ctx, item)
}

func (s *simulationService) GetScenarioByID(ctx context.Context, id string) (*models.Scenario, error) {
	return s.repo.GetScenarioByID(ctx, id)
}

func (s *simulationService) CreateSimulationLog(ctx context.Context, item *models.SimulationLog) error {
	return s.repo.CreateSimulationLog(ctx, item)
}

func (s *simulationService) GetSimulationLogByID(ctx context.Context, id string) (*models.SimulationLog, error) {
	return s.repo.GetSimulationLogByID(ctx, id)
}

func (s *simulationService) CreateSimulationMetric(ctx context.Context, item *models.SimulationMetric) error {
	return s.repo.CreateSimulationMetric(ctx, item)
}

func (s *simulationService) GetSimulationMetricByID(ctx context.Context, id string) (*models.SimulationMetric, error) {
	return s.repo.GetSimulationMetricByID(ctx, id)
}

func (s *simulationService) CreateSimulationTemplate(ctx context.Context, item *models.SimulationTemplate) error {
	return s.repo.CreateSimulationTemplate(ctx, item)
}

func (s *simulationService) GetSimulationTemplateByID(ctx context.Context, id string) (*models.SimulationTemplate, error) {
	return s.repo.GetSimulationTemplateByID(ctx, id)
}
