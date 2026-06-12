package main

import (
	"context"
	"log"
	"net/http"
	"os"

	"engineapp/database"
	_ "engineapp/docs"
	"engineapp/handlers"
	"engineapp/handlers/health"
	"engineapp/handlers/ws"
	"engineapp/kafka"

	httpSwagger "github.com/swaggo/http-swagger"

	"github.com/joho/godotenv"
)

// @title           EngineApp API
// @version         1.0
// @description     This is the Chess Engine App service responsible for game logic and AI moves.
// @host      localhost:8082
// @BasePath  /

func main() {
	port := os.Getenv("ENGINEAPP_HTTP_PORT")
	if port == "" {
		port = "8082"
	}

	log.SetPrefix("[ChessEngine]")
	log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)

	err := godotenv.Load("../.env")
	if err != nil {
		log.Printf("No ../.env file found; assuming variables are provided by the environment.")
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

	mongoUri := os.Getenv("MONGO_HOST")
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
		log.Println("No MONGO_HOST provided, skipping Mongo connection")
	}

	kafkaServers := os.Getenv("KAFKA_BOOTSTRAP_SERVERS")
	if kafkaServers == "" {
		kafkaServers = "localhost:9092"
	}
	var kafkaProducer *kafka.Producer
	kp, err := kafka.NewProducer(kafkaServers)
	if err != nil {
		log.Printf("Failed to initialize Kafka producer: %v", err)
	} else {
		kafkaProducer = kp
		defer kafkaProducer.Close()
	}

	moveHandler := handlers.NewMoveHandler(mongoRepo, kafkaProducer)
	gameHandler := handlers.NewGameHandler(mongoRepo)

	// health check
	http.HandleFunc("GET /health/live", health.Check)
	http.HandleFunc("GET /health/ready", health.Check)

	// swagger
	http.HandleFunc("GET /swagger/", httpSwagger.WrapHandler)

	// websocket
	http.HandleFunc("GET /ws/", ws.HandleConnections(moveHandler.HandleMove, moveHandler.HandleConnect))

	// api
	http.HandleFunc("GET /api/game/board/{gameId}", gameHandler.GetGame)
	http.HandleFunc("POST /api/game/computer", gameHandler.RequestComputerGame)
	http.HandleFunc("POST /api/game/online", gameHandler.RequestOnlineGame)

	log.Printf("Engine HTTP Service running on port %s", port)
	if err := http.ListenAndServe(":"+port, nil); err != nil {
		log.Fatalf("HTTP Server failed to start: %v", err)
	}
}
