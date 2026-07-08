package jobs

import (
	"encoding/json"

	"github.com/hibiken/asynq"
	"github.com/sribash/world-simulation-engine/core-engine/internal/utils"
	"go.uber.org/zap"
)

var Client *asynq.Client

// InitClient initializes the Asynq client for enqueueing jobs
func InitClient(redisURL string) {
	opt, err := asynq.ParseRedisURI(redisURL)
	if err != nil {
		utils.Logger.Error("Failed to parse Redis URI for Asynq. Jobs disabled.", zap.Error(err))
		return
	}

	Client = asynq.NewClient(opt)
}

// EnqueueJob allows any part of the system to push a background task
func EnqueueJob(taskType string, payload interface{}, opts ...asynq.Option) (*asynq.TaskInfo, error) {
	bytes, err := json.Marshal(payload)
	if err != nil {
		return nil, err
	}

	task := asynq.NewTask(taskType, bytes)
	return Client.Enqueue(task, opts...)
}
