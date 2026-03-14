package main

import (
	"log"
	"net/http"
	"os"

	"engineapp/handlers/health"
	"engineapp/handlers/ws"
)

func main() {
	port := os.Getenv("ENGINE_PORT")
	if port == "" {
		port = "8082"
	}

	http.HandleFunc("/health/live", health.Check)
	http.HandleFunc("/health/ready", health.Check)
	http.HandleFunc("/ws/", ws.HandleConnections)

	log.Printf("Engine Service running on port %s", port)
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatalf("Server failed to start: %v", err)
	}
}
