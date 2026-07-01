package api

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/sribash/world-simulation-engine/core-engine/internal/core"
)

// SetupRouter initializes the Gin engine and API routes
func SetupRouter(engine *core.SimulationEngine) *gin.Engine {
	r := gin.Default()

	// Health Check
	r.GET("/api/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{"status": "Core Engine is running"})
	})

	// Simulation Control Group
	sim := r.Group("/api/v1/simulation")
	{
		sim.GET("/status", func(c *gin.Context) {
			c.JSON(http.StatusOK, gin.H{
				"running": engine.IsRunning(),
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
