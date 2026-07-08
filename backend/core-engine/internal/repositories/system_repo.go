package repositories

import (
	"context"
	"github.com/sribash/world-simulation-engine/core-engine/internal/models"
	"gorm.io/gorm"
)

type SystemRepository interface {
	CreateWebhook(ctx context.Context, item *models.Webhook) error
	GetWebhookByID(ctx context.Context, id string) (*models.Webhook, error)
	CreateAuditLog(ctx context.Context, item *models.AuditLog) error
	GetAuditLogByID(ctx context.Context, id string) (*models.AuditLog, error)
	CreateSystemAlert(ctx context.Context, item *models.SystemAlert) error
	GetSystemAlertByID(ctx context.Context, id string) (*models.SystemAlert, error)
}

type systemRepository struct {
	db *gorm.DB
}

func NewSystemRepository(db *gorm.DB) SystemRepository {
	return &systemRepository{db: db}
}

func (r *systemRepository) CreateWebhook(ctx context.Context, item *models.Webhook) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *systemRepository) GetWebhookByID(ctx context.Context, id string) (*models.Webhook, error) {
	var item models.Webhook
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}

func (r *systemRepository) CreateAuditLog(ctx context.Context, item *models.AuditLog) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *systemRepository) GetAuditLogByID(ctx context.Context, id string) (*models.AuditLog, error) {
	var item models.AuditLog
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}

func (r *systemRepository) CreateSystemAlert(ctx context.Context, item *models.SystemAlert) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *systemRepository) GetSystemAlertByID(ctx context.Context, id string) (*models.SystemAlert, error) {
	var item models.SystemAlert
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}
