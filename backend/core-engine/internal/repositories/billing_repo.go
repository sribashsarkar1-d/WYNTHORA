package repositories

import (
	"context"
	"github.com/sribash/world-simulation-engine/core-engine/internal/models"
	"gorm.io/gorm"
)

type BillingRepository interface {
	CreateSubscription(ctx context.Context, item *models.Subscription) error
	GetSubscriptionByID(ctx context.Context, id string) (*models.Subscription, error)
	CreateInvoice(ctx context.Context, item *models.Invoice) error
	GetInvoiceByID(ctx context.Context, id string) (*models.Invoice, error)
	CreatePaymentMethod(ctx context.Context, item *models.PaymentMethod) error
	GetPaymentMethodByID(ctx context.Context, id string) (*models.PaymentMethod, error)
}

type billingRepository struct {
	db *gorm.DB
}

func NewBillingRepository(db *gorm.DB) BillingRepository {
	return &billingRepository{db: db}
}

func (r *billingRepository) CreateSubscription(ctx context.Context, item *models.Subscription) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *billingRepository) GetSubscriptionByID(ctx context.Context, id string) (*models.Subscription, error) {
	var item models.Subscription
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}

func (r *billingRepository) CreateInvoice(ctx context.Context, item *models.Invoice) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *billingRepository) GetInvoiceByID(ctx context.Context, id string) (*models.Invoice, error) {
	var item models.Invoice
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}

func (r *billingRepository) CreatePaymentMethod(ctx context.Context, item *models.PaymentMethod) error {
	return r.db.WithContext(ctx).Create(item).Error
}

func (r *billingRepository) GetPaymentMethodByID(ctx context.Context, id string) (*models.PaymentMethod, error) {
	var item models.PaymentMethod
	err := r.db.WithContext(ctx).First(&item, "id = ?", id).Error
	return &item, err
}
