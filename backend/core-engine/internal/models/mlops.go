package models

import (
	"gorm.io/gorm"
	"time"
)

type MLModel struct {
	ID        string         `gorm:"primaryKey;type:uuid;default:gen_random_uuid()" json:"id"`
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `gorm:"index" json:"-"`
}

type Dataset struct {
	ID        string         `gorm:"primaryKey;type:uuid;default:gen_random_uuid()" json:"id"`
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `gorm:"index" json:"-"`
}
