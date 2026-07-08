package storage

import (
	"context"
	"io"
)

// Provider interface defines the contract for any storage backend
type Provider interface {
	// Upload saves a file to the storage backend and returns the URL/path
	Upload(ctx context.Context, bucket string, filename string, reader io.Reader) (string, error)

	// Download retrieves a file from the storage backend
	Download(ctx context.Context, bucket string, filename string) (io.ReadCloser, error)

	// Delete removes a file from the storage backend
	Delete(ctx context.Context, bucket string, filename string) error

	// GetURL returns a public or presigned URL for the file
	GetURL(ctx context.Context, bucket string, filename string) (string, error)
}
