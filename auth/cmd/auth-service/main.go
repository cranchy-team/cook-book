package main

import (
	"log"

	"github.com/cook-book/auth/internal/config"
	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

// @title           Cook Book Auth API
// @version         1.0
// @description     Сервис аутентификации для приложения Cook Book
// @host            localhost:8000
// @BasePath        /api/v1
func main() {
	cfg := config.Load()

	db, err := gorm.Open(postgres.Open(cfg.DatabaseURL), &gorm.Config{})
	if err != nil {
		log.Fatalf("Ошибка подключения к базе данных: %v", err)
	}

	sqlDB, err := db.DB()
	if err != nil {
		log.Fatalf("Ошибка получения объекта БД: %v", err)
	}
	if err := sqlDB.Ping(); err != nil {
		log.Fatalf("Ошибка пинга БД: %v", err)
	}

	log.Println("Сервис аутентификации запускается...")

	r := gin.Default()

	r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	if err := r.Run(":" + cfg.Port); err != nil {
		log.Fatalf("Ошибка запуска сервера: %v", err)
	}
}
