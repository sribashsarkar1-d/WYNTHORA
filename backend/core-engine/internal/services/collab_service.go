package services

import (
	"context"
	"github.com/sribash/world-simulation-engine/core-engine/internal/models"
	"github.com/sribash/world-simulation-engine/core-engine/internal/repositories"
)

type CollabService interface {
	CreateCollabSession(ctx context.Context, item *models.CollabSession) error
	GetCollabSessionByID(ctx context.Context, id string) (*models.CollabSession, error)
	CreateChatMessage(ctx context.Context, item *models.ChatMessage) error
	GetChatMessageByID(ctx context.Context, id string) (*models.ChatMessage, error)
}

type collabService struct {
	repo repositories.CollabRepository
}

func NewCollabService(repo repositories.CollabRepository) CollabService {
	return &collabService{repo: repo}
}

func (s *collabService) CreateCollabSession(ctx context.Context, item *models.CollabSession) error {
	return s.repo.CreateCollabSession(ctx, item)
}

func (s *collabService) GetCollabSessionByID(ctx context.Context, id string) (*models.CollabSession, error) {
	return s.repo.GetCollabSessionByID(ctx, id)
}

func (s *collabService) CreateChatMessage(ctx context.Context, item *models.ChatMessage) error {
	return s.repo.CreateChatMessage(ctx, item)
}

func (s *collabService) GetChatMessageByID(ctx context.Context, id string) (*models.ChatMessage, error) {
	return s.repo.GetChatMessageByID(ctx, id)
}
