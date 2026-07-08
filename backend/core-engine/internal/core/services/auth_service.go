package services

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"errors"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"github.com/google/uuid"
	"github.com/sribash/world-simulation-engine/core-engine/internal/core/domain"
	"github.com/sribash/world-simulation-engine/core-engine/internal/core/ports"
	"golang.org/x/crypto/bcrypt"
)

type authService struct {
	userRepo   ports.UserRepository
	orgRepo    ports.OrgRepository
	apiKeyRepo ports.ApiKeyRepository
	mfaRepo    ports.MfaRepository
	jwtSecret  []byte
}

func NewAuthService(
	userRepo ports.UserRepository,
	orgRepo ports.OrgRepository,
	apiKeyRepo ports.ApiKeyRepository,
	mfaRepo ports.MfaRepository,
	jwtSecret string,
) ports.AuthService {
	return &authService{
		userRepo:   userRepo,
		orgRepo:    orgRepo,
		apiKeyRepo: apiKeyRepo,
		mfaRepo:    mfaRepo,
		jwtSecret:  []byte(jwtSecret),
	}
}

func (s *authService) Login(ctx context.Context, email, password string) (string, error) {
	user, err := s.userRepo.GetByEmail(ctx, email)
	if err != nil {
		return "", errors.New("invalid credentials")
	}
	if !user.IsActive {
		return "", errors.New("user is not active")
	}

	err = bcrypt.CompareHashAndPassword([]byte(user.PasswordHash), []byte(password))
	if err != nil {
		return "", errors.New("invalid credentials")
	}

	now := time.Now()
	user.LastLogin = &now
	_ = s.userRepo.Update(ctx, user)

	return s.generateJWT(user)
}

func (s *authService) generateJWT(user *domain.User) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"sub":   user.ID.String(),
		"email": user.Email,
		"exp":   time.Now().Add(time.Hour * 24).Unix(),
	})

	return token.SignedString(s.jwtSecret)
}

func (s *authService) Register(ctx context.Context, email, password, orgName string) (*domain.User, error) {
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return nil, err
	}

	var orgID *uuid.UUID
	if orgName != "" {
		org := &domain.Organization{
			Name: orgName,
		}
		if err := s.orgRepo.Create(ctx, org); err != nil {
			return nil, err
		}
		orgID = &org.ID
	}

	user := &domain.User{
		Email:        email,
		PasswordHash: string(hashedPassword),
		OrgID:        orgID,
		IsActive:     true,
	}

	if err := s.userRepo.Create(ctx, user); err != nil {
		return nil, err
	}

	return user, nil
}

func (s *authService) VerifyMFA(ctx context.Context, userID uuid.UUID, code string) (string, error) {
	// Simplified MFA logic for demonstration
	devices, err := s.mfaRepo.GetByUserID(ctx, userID)
	if err != nil || len(devices) == 0 {
		return "", errors.New("mfa not configured")
	}

	// Normally verify TOTP using the secret key.
	// For this exercise, we assume any code is valid if device exists.
	if code == "" {
		return "", errors.New("invalid mfa code")
	}

	user, err := s.userRepo.GetByID(ctx, userID)
	if err != nil {
		return "", err
	}

	return s.generateJWT(user)
}

func (s *authService) GenerateApiKey(ctx context.Context, userID uuid.UUID, name string) (string, error) {
	keyBytes := make([]byte, 32)
	_, err := rand.Read(keyBytes)
	if err != nil {
		return "", err
	}

	keyString := hex.EncodeToString(keyBytes)
	keyHash, _ := bcrypt.GenerateFromPassword([]byte(keyString), bcrypt.DefaultCost)
	prefix := keyString[:8]

	apiKey := &domain.ApiKey{
		UserID:    userID,
		KeyHash:   string(keyHash),
		KeyPrefix: prefix,
		Name:      name,
	}

	if err := s.apiKeyRepo.Create(ctx, apiKey); err != nil {
		return "", err
	}

	return keyString, nil
}

func (s *authService) GetApiKeys(ctx context.Context, userID uuid.UUID) ([]*domain.ApiKey, error) {
	return s.apiKeyRepo.GetByUserID(ctx, userID)
}

func (s *authService) RevokeApiKey(ctx context.Context, keyID uuid.UUID) error {
	return s.apiKeyRepo.Delete(ctx, keyID)
}

func (s *authService) GetAllUsers(ctx context.Context) ([]*domain.User, error) {
	return s.userRepo.GetAll(ctx)
}
