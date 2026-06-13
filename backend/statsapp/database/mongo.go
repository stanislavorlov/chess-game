package database

import (
	"context"
	"log"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var Client *mongo.Client
var StatCollection *mongo.Collection

func ConnectMongoDB(host string, dbName string) error {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	// Connect to local MongoDB by default
	clientOptions := options.Client().ApplyURI(host)

	client, err := mongo.Connect(ctx, clientOptions)
	if err != nil {
		return err
	}

	err = client.Ping(ctx, nil)
	if err != nil {
		return err
	}

	log.Println("Connected to MongoDB!")

	Client = client
	StatCollection = client.Database(dbName).Collection("stats")

	// Ensure indexes on light_player and dark_player to prevent COLLSCAN
	_, err = StatCollection.Indexes().CreateMany(ctx, []mongo.IndexModel{
		{
			Keys: bson.D{{Key: "light_player", Value: 1}},
		},
		{
			Keys: bson.D{{Key: "dark_player", Value: 1}},
		},
	})
	if err != nil {
		log.Printf("Warning: failed to create indexes on StatCollection: %v", err)
	}

	return nil
}

func DisconnectMongoDB() {
	if Client != nil {
		ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()
		if err := Client.Disconnect(ctx); err != nil {
			log.Printf("Failed to disconnect from MongoDB: %v", err)
		} else {
			log.Println("Disconnected from MongoDB.")
		}
	}
}
