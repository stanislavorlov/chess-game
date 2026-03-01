package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"statsapp/database"
	"statsapp/handlers"
	"statsapp/kafka"
	"statsapp/routes"
	"syscall"

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

	// Initialize context for graceful shutdown of background services
	ctx, cancelFunc := context.WithCancel(context.Background())
	defer cancelFunc()

	// Initialize Kafka Consumer
	kafkaServers := os.Getenv("KAFKA_BOOTSTRAP_SERVERS")
	if kafkaServers == "" {
		log.Println("WARNING: KAFKA_BOOTSTRAP_SERVERS not set. Defaulting to localhost:9092")
		kafkaServers = "localhost:9092"
	}

	kafkaTopic := "chess_events"
	consumer, err := kafka.StartConsumer(ctx, kafkaServers, "statsapp_group", kafkaTopic, handlers.HandleChessEvent)
	if err != nil {
		log.Fatalf("Failed to start Kafka consumer: %v", err)
	}
	defer consumer.Close()

	// Handle graceful shutdown signals
	go func() {
		stop := make(chan os.Signal, 1)
		signal.Notify(stop, os.Interrupt, syscall.SIGTERM)
		<-stop
		log.Println("Shutting down gracefully...")
		cancelFunc() // signals the kafka consumer to stop
	}()

	// Setup routes
	router := routes.SetupRouter()

	log.Println("Starting server on port 8081...")
	if err := router.Run(":8081"); err != nil && err != http.ErrServerClosed {
		log.Fatalf("Server error: %s\n", err)
	}
}
