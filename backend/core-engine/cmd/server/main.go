package main

import (
	"context"
	"time"

	"github.com/sribash/world-simulation-engine/core-engine/internal/api"
	"github.com/sribash/world-simulation-engine/core-engine/internal/cache"
	"github.com/sribash/world-simulation-engine/core-engine/internal/config"
	"github.com/sribash/world-simulation-engine/core-engine/internal/core"
	"github.com/sribash/world-simulation-engine/core-engine/internal/infrastructure"
	"github.com/sribash/world-simulation-engine/core-engine/internal/infrastructure/events"
	"github.com/sribash/world-simulation-engine/core-engine/internal/infrastructure/storage"
	"github.com/sribash/world-simulation-engine/core-engine/internal/infrastructure/websocket"
	"github.com/sribash/world-simulation-engine/core-engine/internal/jobs"
	"github.com/sribash/world-simulation-engine/core-engine/internal/utils"
	"go.uber.org/zap"
)

func main() {
	// 1. Load Configuration
	cfg := config.LoadConfig()

	utils.InitLogger(cfg.Env)
	defer utils.Logger.Sync()
	utils.Logger.Info("Starting World Simulation Core Engine", zap.String("env", cfg.Env))

	// 2. Connect to Database and External Services
	infrastructure.ConnectDB(cfg.DBUrl)
	cache.InitRedis(cfg.RedisURL)
	jobs.InitClient(cfg.RedisURL)

	// Start Background Job Worker in a separate goroutine
	jobs.InitWorkerServer(cfg.RedisURL)
	go jobs.StartWorkerServer()

	// 3. Initialize Core Simulation Engine (Tick rate: 1 tick every 5 seconds)
	// In production, you might want this to be 1 second or configurable
	simulationEngine := core.NewSimulationEngine(5 * time.Second)

	// Optional: Auto-start simulation on boot
	// simulationEngine.Start()

	// 4. Initialize Core Infrastructure Components (Phase 4)
	wsHub := websocket.NewHub()
	go wsHub.Run()

	storageProvider := storage.NewLocalStorage("./uploads")
	eventDispatcher := events.NewRedisDispatcher(cache.Client)

	// Wire simulation ticks to event dispatcher
	simulationEngine.OnTick = func() {
		if eventDispatcher != nil {
			eventDispatcher.Publish(context.Background(), "simulation.events", map[string]interface{}{
				"type": "tick",
				"message": "Executing simulation step...",
			})
		}
	}

	// 5. Setup API Router
	router := api.SetupRouter(simulationEngine, cfg.JWTSecret, wsHub, storageProvider, eventDispatcher)

	// 6. Start HTTP Server
	utils.Logger.Info("Server listening", zap.String("port", cfg.Port))
	if err := router.Run(":" + cfg.Port); err != nil {
		utils.Logger.Fatal("Failed to start server", zap.Error(err))
	}
}
