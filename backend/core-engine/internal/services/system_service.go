package services

import (
	"context"
	"github.com/sribash/world-simulation-engine/core-engine/internal/models"
	"github.com/sribash/world-simulation-engine/core-engine/internal/repositories"
)

type SystemService interface {
	CreateWebhook(ctx context.Context, item *models.Webhook) error
	GetWebhookByID(ctx context.Context, id string) (*models.Webhook, error)
	CreateAuditLog(ctx context.Context, item *models.AuditLog) error
	GetAuditLogByID(ctx context.Context, id string) (*models.AuditLog, error)
	CreateSystemAlert(ctx context.Context, item *models.SystemAlert) error
	GetSystemAlertByID(ctx context.Context, id string) (*models.SystemAlert, error)
}

type systemService struct {
	repo repositories.SystemRepository
}

func NewSystemService(repo repositories.SystemRepository) SystemService {
	return &systemService{repo: repo}
}

func (s *systemService) CreateWebhook(ctx context.Context, item *models.Webhook) error {
	return s.repo.CreateWebhook(ctx, item)
}

func (s *systemService) GetWebhookByID(ctx context.Context, id string) (*models.Webhook, error) {
	return s.repo.GetWebhookByID(ctx, id)
}

func (s *systemService) CreateAuditLog(ctx context.Context, item *models.AuditLog) error {
	return s.repo.CreateAuditLog(ctx, item)
}

func (s *systemService) GetAuditLogByID(ctx context.Context, id string) (*models.AuditLog, error) {
	return s.repo.GetAuditLogByID(ctx, id)
}

func (s *systemService) CreateSystemAlert(ctx context.Context, item *models.SystemAlert) error {
	return s.repo.CreateSystemAlert(ctx, item)
}

func (s *systemService) GetSystemAlertByID(ctx context.Context, id string) (*models.SystemAlert, error) {
	return s.repo.GetSystemAlertByID(ctx, id)
}
