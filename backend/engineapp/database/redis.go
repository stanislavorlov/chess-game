package database

import (
	"context"
	"log"
	"time"

	"github.com/go-redis/redis/v8"
)

var RedisClient *redis.Client

func ConnectRedis(url string) error {
	opt, err := redis.ParseURL(url)
	if err != nil {
		return err
	}

	client := redis.NewClient(opt)

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	_, err = client.Ping(ctx).Result()
	if err != nil {
		return err
	}

	log.Println("Connected to Redis!")
	RedisClient = client
	return nil
}

func DisconnectRedis() {
	if RedisClient != nil {
		if err := RedisClient.Close(); err != nil {
			log.Printf("Failed to disconnect from Redis: %v", err)
		} else {
			log.Println("Disconnected from Redis.")
		}
	}
}

// SetGameState writes a serialized board state to Redis with an expiration
func SetGameState(ctx context.Context, gameID string, stateData string) error {
	if RedisClient == nil {
		return redis.Nil
	}
	// Expire an inactive game cache after 2 hours
	return RedisClient.Set(ctx, "game:"+gameID+":state", stateData, 2*time.Hour).Err()
}

// GetGameState attempts to read the state from Redis and return it
func GetGameState(ctx context.Context, gameID string) (string, error) {
	if RedisClient == nil {
		return "", redis.Nil
	}
	val, err := RedisClient.Get(ctx, "game:"+gameID+":state").Result()
	if err != nil {
		return "", err
	}
	return val, nil
}
