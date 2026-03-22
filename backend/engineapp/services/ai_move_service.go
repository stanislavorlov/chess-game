package services

import (
	"context"
	"errors"
	"log"
	"os"

	"engineapp/database"
	pb "engineapp/proto"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func PredictMove(ctx context.Context, gameID string, currentEntry *database.GameHistory) (string, error) {
	// Call Python chessapp via gRPC for AI move
	grpcHost := os.Getenv("CHESSAPP_GRPC_HOST")
	if grpcHost == "" {
		grpcHost = "localhost:50052"
	}

	conn, err := grpc.NewClient(grpcHost, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Printf("Failed to connect to chessapp gRPC: %v", err)
	} else {
		defer conn.Close()
		client := pb.NewAiServiceClient(conn)

		predictResp, err := client.GetPredictedMove(ctx, &pb.PredictedMoveRequest{
			Bitboard:    currentEntry.Bitboard,
			IsWhiteTurn: true,
		})

		if err != nil {
			log.Printf("Failed to call GetPredictedMove via gRPC: %v", err)
		} else {
			log.Printf("Received Predicted Move from Python gRPC: uci_move=%s", predictResp.UciMove)

			return predictResp.UciMove, nil
		}
	}

	return "", errors.New("Failed to get predicted move from chessapp")
}
