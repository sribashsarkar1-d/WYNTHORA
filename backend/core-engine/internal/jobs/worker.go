package jobs

import (
	"context"

	"github.com/hibiken/asynq"
	"github.com/sribash/world-simulation-engine/core-engine/internal/utils"
	"go.uber.org/zap"
)

var Server *asynq.Server
var Mux *asynq.ServeMux

// InitWorkerServer initializes the Asynq Background Job server
func InitWorkerServer(redisURL string) {
	opt, err := asynq.ParseRedisURI(redisURL)
	if err != nil {
		utils.Logger.Error("Failed to parse Redis URI for Asynq Worker. Worker disabled.", zap.Error(err))
		return
	}

	Server = asynq.NewServer(
		opt,
		asynq.Config{
			Concurrency: 10,
			Queues: map[string]int{
				"critical": 6,
				"default":  3,
				"low":      1,
			},
		},
	)

	Mux = asynq.NewServeMux()

	// Example job registration (to be expanded later)
	Mux.HandleFunc("simulation:run", handleSimulationRunTask)
}

// StartWorkerServer starts blocking and processing jobs
func StartWorkerServer() {
	if Server == nil || Mux == nil {
		utils.Logger.Warn("Asynq worker server is disabled (probably due to missing Redis).")
		return
	}

	if err := Server.Run(Mux); err != nil {
		utils.Logger.Error("Failed to run Asynq worker server", zap.Error(err))
	}
}

func handleSimulationRunTask(ctx context.Context, t *asynq.Task) error {
	utils.Logger.Info("Processing simulation:run background job", zap.String("payload", string(t.Payload())))
	// To be implemented fully in Simulation Service
	return nil
}
