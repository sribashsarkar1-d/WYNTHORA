package api

import (
	"context"
	"encoding/json"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"github.com/sribash/world-simulation-engine/core-engine/internal/api/middleware"
	"github.com/sribash/world-simulation-engine/core-engine/internal/core"
	"github.com/sribash/world-simulation-engine/core-engine/internal/infrastructure/events"
	"github.com/sribash/world-simulation-engine/core-engine/internal/infrastructure/storage"
	"github.com/sribash/world-simulation-engine/core-engine/internal/infrastructure/websocket"
)

// SetupRouter initializes the Gin engine and API routes
func SetupRouter(engine *core.SimulationEngine, jwtSecret string, wsHub *websocket.Hub, storageProvider storage.Provider, eventDispatcher events.Dispatcher) *gin.Engine {
	r := gin.New()

	r.Use(gin.Recovery())
	r.Use(middleware.RequestID())
	r.Use(middleware.Logger())
	r.Use(middleware.SecurityHeaders())
	r.Use(middleware.CORSMiddleware())
	r.Use(middleware.PrometheusMetrics())
	r.Use(middleware.RateLimiter(100, 1*time.Minute))

	// Subscribe to simulation updates and broadcast to WebSocket clients
	if eventDispatcher != nil {
		eventDispatcher.Subscribe(context.Background(), "simulation.events", func(payload events.EventPayload) {
			bytes, err := json.Marshal(payload)
			if err == nil {
				wsHub.Broadcast <- bytes
			}
		})
	}

	// Register our REST API routes
	RegisterRestRoutes(r, jwtSecret, wsHub, storageProvider, eventDispatcher)

	// WebSocket endpoint
	r.GET("/ws", func(c *gin.Context) {
		websocket.ServeWs(wsHub, c.Writer, c.Request)
	})
	// Health & Metrics
	r.GET("/health", func(c *gin.Context) { c.JSON(http.StatusOK, gin.H{"status": "ok"}) })
	r.GET("/readiness", func(c *gin.Context) { c.JSON(http.StatusOK, gin.H{"status": "ready"}) })
	r.GET("/liveness", func(c *gin.Context) { c.JSON(http.StatusOK, gin.H{"status": "alive"}) })
	r.GET("/metrics", gin.WrapH(promhttp.Handler()))

	// Simulation Control Group
	sim := r.Group("/api/v1/simulation")
	{
		sim.GET("/status", func(c *gin.Context) {
			c.JSON(http.StatusOK, gin.H{
				"running":   engine.IsRunning(),
				"tick_rate": engine.TickRate.String(),
			})
		})

		sim.POST("/start", func(c *gin.Context) {
			if engine.IsRunning() {
				c.JSON(http.StatusBadRequest, gin.H{"error": "Simulation is already running"})
				return
			}
			engine.Start()
			c.JSON(http.StatusOK, gin.H{"message": "Simulation started"})
		})

		sim.POST("/stop", func(c *gin.Context) {
			if !engine.IsRunning() {
				c.JSON(http.StatusBadRequest, gin.H{"error": "Simulation is not running"})
				return
			}
			engine.Stop()
			c.JSON(http.StatusOK, gin.H{"message": "Simulation stopped"})
		})

		// Manual tick for testing
		sim.POST("/tick", func(c *gin.Context) {
			engine.Tick()
			c.JSON(http.StatusOK, gin.H{"message": "Manual tick executed"})
		})
	}

	return r
}
