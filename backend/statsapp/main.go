package main

import (
	"log"
	"net/http"
	"os"
	"statsapp/database"
	"statsapp/routes"

	"github.com/joho/godotenv"
)

// @title           Stats API
// @version         1.0
// @description     This is a sample server for stats collection.
// @host      localhost:8081
// @BasePath  /api

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Fatalf("Error loading .env file: %v", err)
	}

	dbHost := os.Getenv("MONGO_HOST")
	dbName := os.Getenv("MONGO_DB")

	// Initialize MongoDB connection
	err = database.ConnectMongoDB(dbHost, dbName)
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
