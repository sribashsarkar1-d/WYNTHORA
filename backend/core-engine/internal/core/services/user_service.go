package services

import (
	"context"

	"github.com/google/uuid"
	"github.com/sribash/world-simulation-engine/core-engine/internal/core/domain"
	"github.com/sribash/world-simulation-engine/core-engine/internal/core/ports"
)

type userService struct {
	userRepo ports.UserRepository
}

func NewUserService(userRepo ports.UserRepository) ports.UserService {
	return &userService{
		userRepo: userRepo,
	}
}

func (s *userService) GetProfile(ctx context.Context, userID uuid.UUID) (*domain.User, error) {
	return s.userRepo.GetByID(ctx, userID)
}

func (s *userService) DeleteUser(ctx context.Context, userID uuid.UUID) error {
	return s.userRepo.Delete(ctx, userID)
}
