package storage

import (
	"context"
	"fmt"
	"io"
)

type S3Storage struct {
	// Add AWS S3 client fields here when implementing
	region string
}

func NewS3Storage(region string) Provider {
	return &S3Storage{region: region}
}

func (s *S3Storage) Upload(ctx context.Context, bucket string, filename string, reader io.Reader) (string, error) {
	// Implementation placeholder for AWS SDK
	return fmt.Sprintf("s3://%s/%s", bucket, filename), nil
}

func (s *S3Storage) Download(ctx context.Context, bucket string, filename string) (io.ReadCloser, error) {
	return nil, fmt.Errorf("s3 download not implemented")
}

func (s *S3Storage) Delete(ctx context.Context, bucket string, filename string) error {
	return fmt.Errorf("s3 delete not implemented")
}

func (s *S3Storage) GetURL(ctx context.Context, bucket string, filename string) (string, error) {
	return fmt.Sprintf("https://%s.s3.%s.amazonaws.com/%s", bucket, s.region, filename), nil
}
