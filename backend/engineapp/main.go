package main

import (
	"log"
	"net"
	"net/http"
	"os"

	"engineapp/handlers/health"
	"engineapp/handlers/ws"
	"engineapp/server"
	pb "engineapp/proto"
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

	// Start HTTP server concurrently
	go func() {
		http.HandleFunc("/health/live", health.Check)
		http.HandleFunc("/health/ready", health.Check)
		http.HandleFunc("/ws/", ws.HandleConnections)

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
	pb.RegisterChessEngineServer(grpcServer, server.NewChessEngineServer())
	
	// Register reflection service on gRPC server
	reflection.Register(grpcServer)

	log.Printf("Engine gRPC Service running on port %s", grpcPort)
	if err := grpcServer.Serve(lis); err != nil {
		log.Fatalf("gRPC Server failed to serve: %v", err)
	}
}
