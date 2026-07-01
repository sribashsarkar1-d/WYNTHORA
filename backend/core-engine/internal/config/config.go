package config

import (
	"log"
	"os"

	"github.com/joho/godotenv"
)

// AppConfig holds the application configuration
type AppConfig struct {
	Port  string
	DBUrl string
	Env   string
}

// LoadConfig reads the .env file and populates the AppConfig struct
func LoadConfig() *AppConfig {
	err := godotenv.Load()
	if err != nil {
		log.Println("Warning: No .env file found or could not be loaded, relying on system environment variables")
	}

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080" // Default port
	}

	dbURL := os.Getenv("DB_URL")
	if dbURL == "" {
		log.Fatal("DB_URL environment variable is required")
	}

	env := os.Getenv("ENVIRONMENT")
	if env == "" {
		env = "development"
	}

	return &AppConfig{
		Port:  port,
		DBUrl: dbURL,
		Env:   env,
	}
}
