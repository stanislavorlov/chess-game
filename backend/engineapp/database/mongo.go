package database

import (
	"context"
	"engineapp/factories"
	"engineapp/models"
	"fmt"
	"log"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

const (
	DatabaseName          = "chess_db"
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

	return &MongoRepository{
		client:   client,
		database: client.Database(DatabaseName),
	}, nil
}

// GetGame retrieves a game by its game ID.
func (r *MongoRepository) GetGame(ctx context.Context, gameID string) (*models.Game, error) {
	var state GameState
	coll := r.database.Collection(GameStateCollection)

	err := coll.FindOne(ctx, bson.M{"game_id": gameID}).Decode(&state)
	if err != nil {
		if err == mongo.ErrNoDocuments {
			return nil, nil // Return nil if not found, not an error
		}
		return nil, fmt.Errorf("failed to fetch game state: %w", err)
	}

	// Load just one last entry
	var history GameHistory
	coll = r.database.Collection(GameHistoryCollection)
	err = coll.FindOne(ctx, bson.M{"game_id": gameID}, options.FindOne().SetSort(bson.M{"sequence": -1})).Decode(&history)
	if err != nil {
		if err == mongo.ErrNoDocuments {
			return nil, nil // Return nil if not found, not an error
		}
		return nil, fmt.Errorf("Failed to fetch game history: %w", err)
	}

	game := factories.LoadGame(
		state.ID,
		models.GameStatus(state.Status),
		models.NewGameFormat(state.Format.Name, state.Format.Minutes, state.Format.MoveIncrementMs),
		history.BoardFen,
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
