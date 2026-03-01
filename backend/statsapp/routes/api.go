package routes

import (
	"statsapp/controllers"
	_ "statsapp/docs"

	"github.com/gin-gonic/gin"
	swaggerFiles "github.com/swaggo/files"
	ginSwagger "github.com/swaggo/gin-swagger"
)

func SetupRouter() *gin.Engine {
	router := gin.Default()

	// API Group
	api := router.Group("/api")
	{
		stats := api.Group("/stats")
		{
			stats.POST("", controllers.CreateStat)
			stats.GET("", controllers.GetStats)
		}
	}

	// Swagger Route
	router.GET("/swagger/*any", ginSwagger.WrapHandler(swaggerFiles.Handler))

	return router
}
