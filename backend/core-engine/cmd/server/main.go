package main

import (
	"log"
	"time"

	"github.com/sribash/world-simulation-engine/core-engine/internal/api"
	"github.com/sribash/world-simulation-engine/core-engine/internal/config"
	"github.com/sribash/world-simulation-engine/core-engine/internal/core"
	"github.com/sribash/world-simulation-engine/core-engine/internal/infrastructure"
)

func main() {
	// 1. Load Configuration
	cfg := config.LoadConfig()
	log.Printf("Starting World Simulation Core Engine in %s mode\n", cfg.Env)

	// 2. Connect to Database
	infrastructure.ConnectDB(cfg.DBUrl)

	// 3. Initialize Core Simulation Engine (Tick rate: 1 tick every 5 seconds)
	// In production, you might want this to be 1 second or configurable
	simulationEngine := core.NewSimulationEngine(5 * time.Second)

	// Optional: Auto-start simulation on boot
	// simulationEngine.Start()

	// 4. Setup API Router
	router := api.SetupRouter(simulationEngine)

	// 5. Start HTTP Server
	log.Printf("Server listening on port %s\n", cfg.Port)
	if err := router.Run(":" + cfg.Port); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
