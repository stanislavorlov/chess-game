package database

import (
	"context"
	"engineapp/factories"
	"engineapp/models"
	"fmt"
	"log"
	"os"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

const (
	GameStateCollection   = "game_states"
	GameHistoryCollection = "game_histories"
)

// MongoRepository encapsulates MongoDB operations.
type MongoRepository struct {
	client   *mongo.Client
	database *mongo.Database
}

// ConnectMongo initializes a new MongoDB connection and returns a repository instance.
func ConnectMongo(ctx context.Context, mongoUri string) (*MongoRepository, error) {
	clientOptions := options.Client().ApplyURI(mongoUri)

	client, err := mongo.Connect(ctx, clientOptions)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to MongoDB: %w", err)
	}

	// Check the connection
	if err := client.Ping(ctx, nil); err != nil {
		return nil, fmt.Errorf("failed to ping MongoDB: %w", err)
	}

	log.Println("Connected to MongoDB!")

	dbName := os.Getenv("MONGO_DB")
	if dbName == "" {
		dbName = "chess"
	}

	return &MongoRepository{
		client:   client,
		database: client.Database(dbName),
	}, nil
}

// GetGame retrieves a game by its game ID.
func (r *MongoRepository) GetGame(ctx context.Context, gameID string) (*models.Game, error) {
	var state GameState
	coll := r.database.Collection(GameStateCollection)

	err := coll.FindOne(ctx, bson.M{"_id": gameID}).Decode(&state)
	if err != nil {
		if err == mongo.ErrNoDocuments {
			return nil, nil // Return nil if not found, not an error
		}
		return nil, fmt.Errorf("failed to fetch game state: %w", err)
	}

	// Load all history entries
	var histories []GameHistory
	coll = r.database.Collection(GameHistoryCollection)
	cursor, err := coll.Find(ctx, bson.M{"game_id": gameID}, options.Find().SetSort(bson.M{"sequence": 1}))
	if err != nil {
		return nil, fmt.Errorf("failed to fetch game histories: %w", err)
	}
	defer cursor.Close(ctx)
	if err := cursor.All(ctx, &histories); err != nil {
		return nil, fmt.Errorf("failed to decode game histories: %w", err)
	}

	if len(histories) == 0 {
		return nil, nil // Return nil if not found
	}

	lastFen := histories[len(histories)-1].BoardFen
	var sanMoves []string
	for _, h := range histories {
		if h.SanMove != "" {
			sanMoves = append(sanMoves, h.SanMove)
		}
	}

	game := factories.LoadGame(
		state.ID,
		models.GameStatus(state.Status),
		models.NewGameFormat(state.Format.Name, state.Format.Minutes, state.Format.MoveIncrementMs),
		models.GameMode(state.Mode),
		models.PlayerType(state.Players.LightPlayerId),
		models.PlayerType(state.Players.DarkPlayerId),
		lastFen,
		sanMoves,
		state.Result.Winner)

	return game, nil
}

func (r *MongoRepository) CreateGameState(ctx context.Context, game *GameState) error {
	coll := r.database.Collection(GameStateCollection)
	_, err := coll.InsertOne(ctx, game)
	if err != nil {
		return fmt.Errorf("failed to create game state: %w", err)
	}
	return nil
}

func (r *MongoRepository) UpdateGameStatus(ctx context.Context, gameID string, status models.GameStatus, result string) error {
	coll := r.database.Collection(GameStateCollection)
	update := bson.M{
		"$set": bson.M{
			"status":        string(status),
			"result.winner": result,
			"finished_at":   time.Now(),
		},
	}
	_, err := coll.UpdateOne(ctx, bson.M{"_id": gameID}, update)
	if err != nil {
		return fmt.Errorf("failed to update game status: %w", err)
	}
	return nil
}

func (r *MongoRepository) CreateGameHistory(ctx context.Context, history *GameHistory) error {
	coll := r.database.Collection(GameHistoryCollection)
	_, err := coll.InsertOne(ctx, history)
	if err != nil {
		return fmt.Errorf("failed to create game history: %w", err)
	}
	return nil
}

func (r *MongoRepository) CreateMatchingQueue(ctx context.Context, queueItem *MatchingQueue) error {
	coll := r.database.Collection("matching_queues") // or whatever collection name is appropriate
	_, err := coll.InsertOne(ctx, queueItem)
	if err != nil {
		return fmt.Errorf("failed to create matching queue: %w", err)
	}
	return nil
}

// Disconnect closes the MongoDB connection.
func (r *MongoRepository) Disconnect(ctx context.Context) error {
	if r.client != nil {
		if err := r.client.Disconnect(ctx); err != nil {
			return fmt.Errorf("failed to disconnect from MongoDB: %w", err)
		}
		log.Println("Disconnected from MongoDB")
	}
	return nil
}
