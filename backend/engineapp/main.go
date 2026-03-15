package main

import (
	"log"
	"net"
	"net/http"
	"os"

	"engineapp/database"
	"engineapp/handlers"
	"engineapp/handlers/health"
	"engineapp/handlers/ws"

	"github.com/joho/godotenv"

	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

func main() {
	port := os.Getenv("ENGINE_PORT")
	if port == "" {
		port = "8082"
	}

	grpcPort := os.Getenv("GRPC_PORT")
	if grpcPort == "" {
		grpcPort = "50051"
	}

	log.SetPrefix("[ChessEngine]")
	log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)

	err := godotenv.Load()
	if err != nil {
		log.Println("No .env file found; assuming variables are provided by the environment.")
	}

	mongoURI := os.Getenv("MONGO_HOST")
	if mongoURI == "" {
		log.Fatal("Failed to get MONGO_HOST from environment variables")
	}

	mongoDBName := os.Getenv("MONGO_DB")
	if mongoDBName == "" {
		log.Fatal("Failed to get MONGO_DB from environment variables")
	}

	// Initialize MongoDB Connection
	if err := database.ConnectMongoDB(mongoURI, mongoDBName); err != nil {
		log.Fatalf("Failed to connect to MongoDB: %v", err)
	}
	defer database.DisconnectMongoDB()

	// Start HTTP server concurrently
	go func() {
		http.HandleFunc("/health/live", health.Check)
		http.HandleFunc("/health/ready", health.Check)
		http.HandleFunc("/ws/", ws.HandleConnections(handlers.HandleMove))

		log.Printf("Engine HTTP Service running on port %s", port)
		if err := http.ListenAndServe(":"+port, nil); err != nil {
			log.Fatalf("HTTP Server failed to start: %v", err)
		}
	}()

	// Start gRPC server
	lis, err := net.Listen("tcp", ":"+grpcPort)
	if err != nil {
		log.Fatalf("failed to listen on port %s: %v", grpcPort, err)
	}

	grpcServer := grpc.NewServer()

	// Register reflection service on gRPC server
	reflection.Register(grpcServer)

	log.Printf("Engine gRPC Service running on port %s", grpcPort)
	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("gRPC Server failed to serve: %v", err)
	}
}
