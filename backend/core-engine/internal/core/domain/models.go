package domain

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

type Organization struct {
	ID               uuid.UUID `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey"`
	Name             string    `gorm:"type:varchar(255);not null"`
	Domain           string    `gorm:"type:varchar(255)"`
	SubscriptionTier string    `gorm:"type:public.sub_tier;default:'FREE'"`
	CreatedAt        time.Time `gorm:"default:CURRENT_TIMESTAMP"`
	UpdatedAt        time.Time `gorm:"default:CURRENT_TIMESTAMP"`
}

type Role struct {
	ID          uuid.UUID `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey"`
	Name        string    `gorm:"type:public.role_type;not null"`
	Description string    `gorm:"type:text"`
}

type User struct {
	ID           uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey"`
	OrgID        *uuid.UUID `gorm:"type:uuid"`
	RoleID       *uuid.UUID `gorm:"type:uuid"`
	Email        string     `gorm:"type:varchar(255);not null"`
	PasswordHash string     `gorm:"type:varchar(255);not null"`
	IsActive     bool       `gorm:"default:true"`
	LastLogin    *time.Time `gorm:"type:timestamp with time zone"`
	CreatedAt    time.Time  `gorm:"default:CURRENT_TIMESTAMP"`
}

type UserMfaDevice struct {
	ID         uuid.UUID `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey"`
	UserID     uuid.UUID `gorm:"type:uuid"`
	DeviceName string    `gorm:"type:varchar(100)"`
	SecretKey  string    `gorm:"type:varchar(255);not null"`
	IsVerified bool      `gorm:"default:false"`
	CreatedAt  time.Time `gorm:"default:CURRENT_TIMESTAMP"`
}

type ApiKey struct {
	ID         uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey"`
	UserID     uuid.UUID  `gorm:"type:uuid"`
	KeyHash    string     `gorm:"type:varchar(255);not null"`
	KeyPrefix  string     `gorm:"type:varchar(10);not null"`
	Name       string     `gorm:"type:varchar(100)"`
	LastUsedAt *time.Time `gorm:"type:timestamp with time zone"`
	ExpiresAt  *time.Time `gorm:"type:timestamp with time zone"`
	IsRevoked  bool       `gorm:"default:false"`
}

type OrganizationInvite struct {
	ID        uuid.UUID  `gorm:"type:uuid;default:public.uuid_generate_v4();primaryKey"`
	OrgID     uuid.UUID  `gorm:"type:uuid;not null"`
	Email     string     `gorm:"type:varchar(255);not null"`
	Token     string     `gorm:"type:varchar(255);not null"`
	RoleID    *uuid.UUID `gorm:"type:uuid"`
	ExpiresAt time.Time  `gorm:"type:timestamp with time zone;not null"`
	CreatedAt time.Time  `gorm:"default:CURRENT_TIMESTAMP"`
}

// BeforeCreate hooks for UUID generation using google/uuid in Go if not handled by DB default
func (u *User) BeforeCreate(tx *gorm.DB) (err error) {
	if u.ID == uuid.Nil {
		u.ID = uuid.New()
	}
	return
}

func (o *Organization) BeforeCreate(tx *gorm.DB) (err error) {
	if o.ID == uuid.Nil {
		o.ID = uuid.New()
	}
	return
}

func (i *OrganizationInvite) BeforeCreate(tx *gorm.DB) (err error) {
	if i.ID == uuid.Nil {
		i.ID = uuid.New()
	}
	return
}

func (a *ApiKey) BeforeCreate(tx *gorm.DB) (err error) {
	if a.ID == uuid.Nil {
		a.ID = uuid.New()
	}
	return
}

func (m *UserMfaDevice) BeforeCreate(tx *gorm.DB) (err error) {
	if m.ID == uuid.Nil {
		m.ID = uuid.New()
	}
	return
}
