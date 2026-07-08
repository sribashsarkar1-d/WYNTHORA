package storage

import (
	"context"
	"fmt"
	"io"
	"os"
	"path/filepath"
)

type LocalStorage struct {
	basePath string
}

func NewLocalStorage(basePath string) Provider {
	// Ensure base directory exists
	if err := os.MkdirAll(basePath, os.ModePerm); err != nil {
		panic(fmt.Sprintf("failed to create local storage base path: %v", err))
	}
	return &LocalStorage{basePath: basePath}
}

func (l *LocalStorage) getPath(bucket, filename string) string {
	return filepath.Join(l.basePath, bucket, filename)
}

func (l *LocalStorage) Upload(ctx context.Context, bucket string, filename string, reader io.Reader) (string, error) {
	fullPath := l.getPath(bucket, filename)

	if err := os.MkdirAll(filepath.Dir(fullPath), os.ModePerm); err != nil {
		return "", err
	}

	dst, err := os.Create(fullPath)
	if err != nil {
		return "", err
	}
	defer dst.Close()

	if _, err := io.Copy(dst, reader); err != nil {
		return "", err
	}

	return fullPath, nil
}

func (l *LocalStorage) Download(ctx context.Context, bucket string, filename string) (io.ReadCloser, error) {
	return os.Open(l.getPath(bucket, filename))
}

func (l *LocalStorage) Delete(ctx context.Context, bucket string, filename string) error {
	return os.Remove(l.getPath(bucket, filename))
}

func (l *LocalStorage) GetURL(ctx context.Context, bucket string, filename string) (string, error) {
	// For local storage, we just return a local path or a local HTTP route if serving statically
	return fmt.Sprintf("/uploads/%s/%s", bucket, filename), nil
}
