package services

import (
	"context"
	"github.com/sribash/world-simulation-engine/core-engine/internal/models"
	"github.com/sribash/world-simulation-engine/core-engine/internal/repositories"
)

type ChatService interface {
	CreateChatThread(ctx context.Context, item *models.ChatThread) error
	GetChatThreadByID(ctx context.Context, id string) (*models.ChatThread, error)
	CreateChatPrompt(ctx context.Context, item *models.ChatPrompt) error
	GetChatPromptByID(ctx context.Context, id string) (*models.ChatPrompt, error)
}

type chatService struct {
	repo repositories.ChatRepository
}

func NewChatService(repo repositories.ChatRepository) ChatService {
	return &chatService{repo: repo}
}

func (s *chatService) CreateChatThread(ctx context.Context, item *models.ChatThread) error {
	return s.repo.CreateChatThread(ctx, item)
}

func (s *chatService) GetChatThreadByID(ctx context.Context, id string) (*models.ChatThread, error) {
	return s.repo.GetChatThreadByID(ctx, id)
}

func (s *chatService) CreateChatPrompt(ctx context.Context, item *models.ChatPrompt) error {
	return s.repo.CreateChatPrompt(ctx, item)
}

func (s *chatService) GetChatPromptByID(ctx context.Context, id string) (*models.ChatPrompt, error) {
	return s.repo.GetChatPromptByID(ctx, id)
}
