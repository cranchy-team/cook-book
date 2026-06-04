package main

import (
	"log"
	"time"

	_ "github.com/cook-book/auth/docs"
	"github.com/cook-book/auth/internal/config"
	"github.com/cook-book/auth/internal/handler"
	"github.com/cook-book/auth/internal/middleware"
	"github.com/cook-book/auth/internal/repository"
	"github.com/cook-book/auth/internal/service"
	"github.com/gin-contrib/cors"
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
// @securityDefinitions.apikey ApiKeyAuth
// @in cookie
// @name access_token
func main() {
	cfg := config.Load()

	db, err := gorm.Open(postgres.Open(cfg.DatabaseURL), &gorm.Config{})
	if err != nil {
		log.Fatalf("Ошибка подключения к базе данных: %v", err)
	}

	log.Println("Сервис аутентификации запускается...")

	userRepo := repository.NewUserRepository(db)
	userService := service.NewUserService(userRepo, cfg.JWTSecret)
	authHandler := handler.NewAuthHandler(userService)
	authMiddleware := middleware.NewAuthMiddleware(userService)

	r := gin.Default()

	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:80", "http://localhost"},
		AllowMethods:     []string{"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Authorization", "Accept"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		MaxAge:           12 * time.Hour,
	}))

	api := r.Group("/api/v1")
	{
		auth := api.Group("/auth")
		{
			auth.POST("/register", authHandler.Register)
			auth.POST("/login", authHandler.Login)
			auth.POST("/logout", authHandler.Logout)

			protected := auth.Group("/")
			protected.Use(authMiddleware.RequireAuth())
			{
				protected.GET("/profile", authHandler.GetProfile)
				protected.POST("/change-password", authHandler.ChangePassword)
			}
		}
	}

	r.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	if err := r.Run(":" + cfg.Port); err != nil {
		log.Fatalf("Ошибка запуска сервера: %v", err)
	}
}
