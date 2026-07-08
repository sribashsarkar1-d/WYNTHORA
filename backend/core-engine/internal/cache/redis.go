package cache

import (
	"context"
	"time"

	"github.com/redis/go-redis/v9"
	"github.com/sribash/world-simulation-engine/core-engine/internal/utils"
	"go.uber.org/zap"
)

var Client *redis.Client

func InitRedis(redisURL string) {
	opt, err := redis.ParseURL(redisURL)
	if err != nil {
		utils.Logger.Fatal("Failed to parse Redis URL", zap.Error(err))
	}

	Client = redis.NewClient(opt)

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	_, err = Client.Ping(ctx).Result()
	if err != nil {
		utils.Logger.Error("Failed to connect to Redis. Rate limiting and jobs will be disabled.", zap.Error(err))
		Client = nil
		return
	}

	utils.Logger.Info("Successfully connected to Redis")
}

func Get(ctx context.Context, key string) (string, error) {
	return Client.Get(ctx, key).Result()
}

func Set(ctx context.Context, key string, value interface{}, expiration time.Duration) error {
	return Client.Set(ctx, key, value, expiration).Err()
}

func Delete(ctx context.Context, key string) error {
	return Client.Del(ctx, key).Err()
}
