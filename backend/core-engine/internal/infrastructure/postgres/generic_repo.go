package postgres

import (
	"context"
	"errors"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// GenericRepo is a generic repository for standard CRUD operations on GORM models.
type GenericRepo[T any] struct {
	db *gorm.DB
}

func NewGenericRepo[T any](db *gorm.DB) *GenericRepo[T] {
	return &GenericRepo[T]{db: db}
}

// Create inserts a new record.
func (r *GenericRepo[T]) Create(ctx context.Context, entity *T) error {
	return r.db.WithContext(ctx).Create(entity).Error
}

// GetByID fetches a record by its UUID.
func (r *GenericRepo[T]) GetByID(ctx context.Context, id uuid.UUID) (*T, error) {
	var entity T
	if err := r.db.WithContext(ctx).First(&entity, "id = ?", id).Error; err != nil {
		if errors.Is(err, gorm.ErrRecordNotFound) {
			return nil, nil // Or a specific not found error
		}
		return nil, err
	}
	return &entity, nil
}

// List fetches a list of records with basic pagination.
func (r *GenericRepo[T]) List(ctx context.Context, limit, offset int, conditions map[string]interface{}) ([]*T, error) {
	var entities []*T
	query := r.db.WithContext(ctx)

	for k, v := range conditions {
		query = query.Where(k, v)
	}

	if limit > 0 {
		query = query.Limit(limit)
	}
	if offset > 0 {
		query = query.Offset(offset)
	}

	if err := query.Find(&entities).Error; err != nil {
		return nil, err
	}
	return entities, nil
}

// Update updates an existing record.
func (r *GenericRepo[T]) Update(ctx context.Context, entity *T) error {
	return r.db.WithContext(ctx).Save(entity).Error
}

// Delete removes a record by its UUID.
func (r *GenericRepo[T]) Delete(ctx context.Context, id uuid.UUID) error {
	var entity T
	return r.db.WithContext(ctx).Delete(&entity, "id = ?", id).Error
}
