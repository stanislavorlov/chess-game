package database

import (
	"context"
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

// GetGameState retrieves a game state by its game ID.
func (r *MongoRepository) GetGameState(ctx context.Context, gameID string) (*GameState, error) {
	var state GameState
	coll := r.database.Collection(GameStateCollection)

	err := coll.FindOne(ctx, bson.M{"game_id": gameID}).Decode(&state)
	if err != nil {
		if err == mongo.ErrNoDocuments {
			return nil, nil // Return nil if not found, not an error
		}
		return nil, fmt.Errorf("failed to fetch game state: %w", err)
	}

	return &state, nil
}

func (r *MongoRepository) CreateGameState(ctx context.Context, game *GameState) error {
	coll := r.database.Collection(GameStateCollection)
	_, err := coll.InsertOne(ctx, game)
	if err != nil {
		return fmt.Errorf("failed to create game state: %w", err)
	}
	return nil
}

// GetGameHistory retrieves all history records for a given game ID, sorted by sequence.
func (r *MongoRepository) GetGameHistory(ctx context.Context, gameID string) ([]GameHistory, error) {
	coll := r.database.Collection(GameHistoryCollection)

	// Use Find to get all documents, sorted by sequence
	opts := options.Find().SetSort(bson.M{"sequence": 1})
	cursor, err := coll.Find(ctx, bson.M{"game_id": gameID}, opts)
	if err != nil {
		return nil, fmt.Errorf("failed to fetch game history: %w", err)
	}
	defer cursor.Close(ctx)

	var history []GameHistory
	if err := cursor.All(ctx, &history); err != nil {
		return nil, fmt.Errorf("failed to decode game history: %w", err)
	}

	return history, nil
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
