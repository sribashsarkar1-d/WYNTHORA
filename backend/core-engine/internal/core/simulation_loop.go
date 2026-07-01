package core

import (
	"log"
	"sync"
	"time"
)

// SimulationEngine manages the core loop of the world simulation
type SimulationEngine struct {
	ticker  *time.Ticker
	quit    chan struct{}
	running bool
	mu      sync.Mutex
	TickRate time.Duration
}

// NewSimulationEngine initializes a new engine
func NewSimulationEngine(tickRate time.Duration) *SimulationEngine {
	return &SimulationEngine{
		TickRate: tickRate,
		quit:     make(chan struct{}),
	}
}

// Start begins the simulation loop
func (se *SimulationEngine) Start() {
	se.mu.Lock()
	if se.running {
		se.mu.Unlock()
		log.Println("Simulation is already running")
		return
	}
	se.running = true
	se.ticker = time.NewTicker(se.TickRate)
	se.mu.Unlock()

	log.Printf("Simulation started with a tick rate of %v\n", se.TickRate)

	go func() {
		for {
			select {
			case <-se.ticker.C:
				se.Tick()
			case <-se.quit:
				se.ticker.Stop()
				return
			}
		}
	}()
}

// Stop halts the simulation loop
func (se *SimulationEngine) Stop() {
	se.mu.Lock()
	defer se.mu.Unlock()
	if !se.running {
		log.Println("Simulation is not running")
		return
	}
	se.running = false
	close(se.quit)
	// Re-initialize quit channel for future restarts
	se.quit = make(chan struct{})
	log.Println("Simulation stopped")
}

// Tick executes a single step of the simulation
func (se *SimulationEngine) Tick() {
	// In the future, this will:
	// 1. Fetch AI Model Predictions
	// 2. Update Agent States (ABM)
	// 3. Update Macro-Economy (System Dynamics)
	// 4. Save state checkpoint to Database

	log.Println("[TICK] Executing simulation step...")
}

// IsRunning returns the current status
func (se *SimulationEngine) IsRunning() bool {
	se.mu.Lock()
	defer se.mu.Unlock()
	return se.running
}
