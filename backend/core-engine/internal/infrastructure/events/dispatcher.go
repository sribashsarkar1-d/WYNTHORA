package events

import (
	"context"
	"encoding/json"
	"time"

	"github.com/google/uuid"
	"github.com/redis/go-redis/v9"
	"github.com/sribash/world-simulation-engine/core-engine/internal/utils"
	"go.uber.org/zap"
)

type Dispatcher interface {
	Publish(ctx context.Context, topic string, data interface{}) error
	Subscribe(ctx context.Context, topic string, handler func(EventPayload)) error
}

type RedisDispatcher struct {
	client *redis.Client
}

func NewRedisDispatcher(client *redis.Client) Dispatcher {
	return &RedisDispatcher{client: client}
}

func (d *RedisDispatcher) Publish(ctx context.Context, topic string, data interface{}) error {
	if d.client == nil {
		utils.Logger.Warn("Redis client is nil. Skipping event publish.", zap.String("topic", topic))
		return nil
	}

	payload := EventPayload{
		EventID:   uuid.New().String(),
		Timestamp: time.Now().Unix(),
		Data:      data,
	}

	bytes, err := json.Marshal(payload)
	if err != nil {
		return err
	}

	return d.client.Publish(ctx, topic, bytes).Err()
}

func (d *RedisDispatcher) Subscribe(ctx context.Context, topic string, handler func(EventPayload)) error {
	if d.client == nil {
		utils.Logger.Warn("Redis client is nil. Skipping event subscribe.", zap.String("topic", topic))
		return nil
	}

	pubsub := d.client.Subscribe(ctx, topic)

	go func() {
		defer pubsub.Close()
		ch := pubsub.Channel()
		for msg := range ch {
			var payload EventPayload
			if err := json.Unmarshal([]byte(msg.Payload), &payload); err != nil {
				utils.Logger.Error("Failed to unmarshal event payload", zap.Error(err))
				continue
			}
			handler(payload)
		}
	}()

	return nil
}
