package main

import (
	"context"
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
	port := os.Getenv("ENGINEAPP_HTTP_PORT")
	if port == "" {
		port = "8082"
	}

	grpcPort := os.Getenv("ENGINEAPP_GRPC_PORT")
	if grpcPort == "" {
		grpcPort = "50051"
	}

	log.SetPrefix("[ChessEngine]")
	log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)

	err := godotenv.Load("../.env")
	if err != nil {
		log.Println("No ../.env file found; assuming variables are provided by the environment.")
	}

	redisURL := os.Getenv("REDIS_URL")
	if redisURL != "" {
		if err := database.ConnectRedis(redisURL); err != nil {
			log.Printf("Failed to connect to Redis initially: %v", err)
		} else {
			defer database.DisconnectRedis()
		}
	} else {
		log.Println("No REDIS_URL provided, skipping Redis connection")
	}

	mongoUri := os.Getenv("MONGO_URI")
	ctx := context.Background()
	var mongoRepo *database.MongoRepository
	if mongoUri != "" {
		var err error
		mongoRepo, err = database.ConnectMongo(ctx, mongoUri)
		if err != nil {
			log.Printf("Failed to connect to Mongo initially: %v", err)
		} else {
			defer mongoRepo.Disconnect(ctx)
		}
	} else {
		log.Println("No MONGO_URI provided, skipping Mongo connection")
	}

	moveHandler := handlers.NewMoveHandler(mongoRepo)

	// Start HTTP server concurrently
	go func() {
		http.HandleFunc("/health/live", health.Check)
		http.HandleFunc("/health/ready", health.Check)
		http.HandleFunc("/ws/", ws.HandleConnections(moveHandler.HandleMove))

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
