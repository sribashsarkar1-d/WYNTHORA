package events

// Common Event Topics
const (
	TopicSimulationCompleted = "simulation:completed"
	TopicSimulationFailed    = "simulation:failed"
	TopicModelTrained        = "model:trained"
	TopicUserRegistered      = "user:registered"
)

// EventPayload defines the standard payload structure for all events
type EventPayload struct {
	EventID   string      `json:"event_id"`
	Timestamp int64       `json:"timestamp"`
	Data      interface{} `json:"data"`
}
