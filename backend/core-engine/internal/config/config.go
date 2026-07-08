package config

import (
	"log"
	"os"

	"github.com/joho/godotenv"
)

// AppConfig holds the application configuration
type AppConfig struct {
	Port             string
	DBUrl            string
	RedisURL         string
	Env              string
	JWTSecret        string
	StorageProvider  string
	StorageLocalPath string
}

// LoadConfig reads the .env file and populates the AppConfig struct
func LoadConfig() *AppConfig {
	env := os.Getenv("ENVIRONMENT")
	if env == "" {
		env = "development"
	}

	envFile := ".env." + env
	godotenv.Load(envFile)
	godotenv.Load() // Fallback to .env

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080" // Default port
	}

	dbURL := os.Getenv("DB_URL")
	if dbURL == "" {
		log.Fatal("DB_URL environment variable is required")
	}

	redisURL := os.Getenv("REDIS_URL")
	if redisURL == "" {
		redisURL = "redis://localhost:6379/0"
	}

	jwtSecret := os.Getenv("JWT_SECRET")
	if jwtSecret == "" {
		jwtSecret = "supersecretdefault" // default for dev
	}

	storageProvider := os.Getenv("STORAGE_PROVIDER")
	if storageProvider == "" {
		storageProvider = "local"
	}

	storageLocalPath := os.Getenv("STORAGE_LOCAL_PATH")
	if storageLocalPath == "" {
		storageLocalPath = "./uploads"
	}

	return &AppConfig{
		Port:             port,
		DBUrl:            dbURL,
		RedisURL:         redisURL,
		Env:              env,
		JWTSecret:        jwtSecret,
		StorageProvider:  storageProvider,
		StorageLocalPath: storageLocalPath,
	}
}
