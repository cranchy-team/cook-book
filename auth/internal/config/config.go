package config

import (
	"log"
	"os"

	"github.com/joho/godotenv"
)

type Config struct {
	DatabaseURL string
	JWTSecret   string
	Port        string
}

func Load() *Config {
	_ = godotenv.Load()

	return &Config{
		DatabaseURL: getEnv("DATABASE_URL", "postgres://postgres:postgres@localhost:5432/cook_book?sslmode=disable"),
		JWTSecret:   getEnv("JWT_SECRET", ""),
		Port:        getEnv("AUTH_SERVICE_PORT", "8000"),
	}
}

func getEnv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	if fallback == "" {
		log.Fatalf("Переменная окружения %s не задана", key)
	}
	return fallback
}
