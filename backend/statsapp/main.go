package main

import (
	"log"
	"net/http"
	"statsapp/database"
	"statsapp/routes"
)

// @title           Stats API
// @version         1.0
// @description     This is a sample server for stats collection.
// @host      localhost:8081
// @BasePath  /api

func main() {
	// Initialize MongoDB connection
	err := database.ConnectMongoDB()
	if err != nil {
		log.Fatalf("Failed to connect to MongoDB: %v", err)
	}

	defer database.DisconnectMongoDB()

	// Setup routes
	router := routes.SetupRouter()

	log.Println("Starting server on port 8081...")
	if err := router.Run(":8081"); err != nil && err != http.ErrServerClosed {
		log.Fatalf("Server error: %s\n", err)
	}
}
