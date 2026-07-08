package services

import (
	"context"
	"github.com/sribash/world-simulation-engine/core-engine/internal/models"
	"github.com/sribash/world-simulation-engine/core-engine/internal/repositories"
)

type BillingService interface {
	CreateSubscription(ctx context.Context, item *models.Subscription) error
	GetSubscriptionByID(ctx context.Context, id string) (*models.Subscription, error)
	CreateInvoice(ctx context.Context, item *models.Invoice) error
	GetInvoiceByID(ctx context.Context, id string) (*models.Invoice, error)
	CreatePaymentMethod(ctx context.Context, item *models.PaymentMethod) error
	GetPaymentMethodByID(ctx context.Context, id string) (*models.PaymentMethod, error)
}

type billingService struct {
	repo repositories.BillingRepository
}

func NewBillingService(repo repositories.BillingRepository) BillingService {
	return &billingService{repo: repo}
}

func (s *billingService) CreateSubscription(ctx context.Context, item *models.Subscription) error {
	return s.repo.CreateSubscription(ctx, item)
}

func (s *billingService) GetSubscriptionByID(ctx context.Context, id string) (*models.Subscription, error) {
	return s.repo.GetSubscriptionByID(ctx, id)
}

func (s *billingService) CreateInvoice(ctx context.Context, item *models.Invoice) error {
	return s.repo.CreateInvoice(ctx, item)
}

func (s *billingService) GetInvoiceByID(ctx context.Context, id string) (*models.Invoice, error) {
	return s.repo.GetInvoiceByID(ctx, id)
}

func (s *billingService) CreatePaymentMethod(ctx context.Context, item *models.PaymentMethod) error {
	return s.repo.CreatePaymentMethod(ctx, item)
}

func (s *billingService) GetPaymentMethodByID(ctx context.Context, id string) (*models.PaymentMethod, error) {
	return s.repo.GetPaymentMethodByID(ctx, id)
}
