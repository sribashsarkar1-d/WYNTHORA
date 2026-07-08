package repositories

import (
	"context"
	"github.com/sribash/world-simulation-engine/core-engine/internal/models"
	"gorm.io/gorm"
)

type CollabRepository interface {
	CreateCollabSession(ctx context.Context, item *models.CollabSession) error
	GetCollabSessionByID(ctx context.Context, id string) (*models.CollabSession, error)
	CreateChatMessage(ctx context.Context, item *models.ChatMessage) error
	GetChatMessageByID(ctx context.Context, id string) (*models.ChatMessage, error)
}

type collabRepository struct {
	db *gorm.DB
}

func NewCollabRepository(db *gorm.DB) CollabRepository {
	return &collabRepository{db: db}
}

func (r *collabRepository) CreateCollabSession(ctx context.Context, item *models.CollabSession) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *collabRepository) GetCollabSessionByID(ctx context.Context, id string) (*models.CollabSession, error) {
	var item models.CollabSession
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}

func (r *collabRepository) CreateChatMessage(ctx context.Context, item *models.ChatMessage) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *collabRepository) GetChatMessageByID(ctx context.Context, id string) (*models.ChatMessage, error) {
	var item models.ChatMessage
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}
