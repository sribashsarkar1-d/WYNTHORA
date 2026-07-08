package services

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"errors"
	"time"

	"github.com/google/uuid"
	"github.com/sribash/world-simulation-engine/core-engine/internal/core/domain"
	"github.com/sribash/world-simulation-engine/core-engine/internal/core/ports"
)

type orgService struct {
	userRepo   ports.UserRepository
	inviteRepo ports.OrgInviteRepository
	roleRepo   ports.RoleRepository
}

func NewOrgService(
	userRepo ports.UserRepository,
	inviteRepo ports.OrgInviteRepository,
	roleRepo ports.RoleRepository,
) ports.OrgService {
	return &orgService{
		userRepo:   userRepo,
		inviteRepo: inviteRepo,
		roleRepo:   roleRepo,
	}
}

func (s *orgService) GetMembers(ctx context.Context, orgID uuid.UUID) ([]*domain.User, error) {
	return s.userRepo.GetByOrgID(ctx, orgID)
}

func (s *orgService) CreateInvite(ctx context.Context, orgID uuid.UUID, email, roleName string) (*domain.OrganizationInvite, error) {
	var roleID *uuid.UUID
	if roleName != "" {
		role, err := s.roleRepo.GetByName(ctx, roleName)
		if err == nil && role != nil {
			roleID = &role.ID
		}
	}

	tokenBytes := make([]byte, 32)
	_, _ = rand.Read(tokenBytes)
	token := hex.EncodeToString(tokenBytes)

	invite := &domain.OrganizationInvite{
		OrgID:     orgID,
		Email:     email,
		Token:     token,
		RoleID:    roleID,
		ExpiresAt: time.Now().Add(time.Hour * 72),
	}

	if err := s.inviteRepo.Create(ctx, invite); err != nil {
		return nil, err
	}
	return invite, nil
}

func (s *orgService) UpdateUserRole(ctx context.Context, orgID, userID uuid.UUID, roleName string) error {
	user, err := s.userRepo.GetByID(ctx, userID)
	if err != nil {
		return err
	}

	if user.OrgID == nil || *user.OrgID != orgID {
		return errors.New("user does not belong to this organization")
	}

	role, err := s.roleRepo.GetByName(ctx, roleName)
	if err != nil {
		return errors.New("invalid role")
	}

	user.RoleID = &role.ID
	return s.userRepo.Update(ctx, user)
}
