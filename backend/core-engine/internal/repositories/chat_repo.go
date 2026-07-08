package repositories

import (
	"context"
	"github.com/sribash/world-simulation-engine/core-engine/internal/models"
	"gorm.io/gorm"
)

type ChatRepository interface {
	CreateChatThread(ctx context.Context, item *models.ChatThread) error
	GetChatThreadByID(ctx context.Context, id string) (*models.ChatThread, error)
	CreateChatPrompt(ctx context.Context, item *models.ChatPrompt) error
	GetChatPromptByID(ctx context.Context, id string) (*models.ChatPrompt, error)
}

type chatRepository struct {
	db *gorm.DB
}

func NewChatRepository(db *gorm.DB) ChatRepository {
	return &chatRepository{db: db}
}

func (r *chatRepository) CreateChatThread(ctx context.Context, item *models.ChatThread) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *chatRepository) GetChatThreadByID(ctx context.Context, id string) (*models.ChatThread, error) {
	var item models.ChatThread
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}

func (r *chatRepository) CreateChatPrompt(ctx context.Context, item *models.ChatPrompt) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *chatRepository) GetChatPromptByID(ctx context.Context, id string) (*models.ChatPrompt, error) {
	var item models.ChatPrompt
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}
