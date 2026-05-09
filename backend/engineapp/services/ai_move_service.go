package services

import (
	"context"
	"errors"
	"log"
	"os"

	"engineapp/models"
	pb "engineapp/proto"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func PredictMove(ctx context.Context, gameID string, bitboards models.Bitboards, isWhiteTurn bool) (string, error) {
	// Call Python chessapp via gRPC for AI move
	grpcHost := os.Getenv("CHESSAPP_GRPC_HOST")
	if grpcHost == "" {
		return "", errors.New("CHESSAPP_GRPC_HOST not set")
	}

	conn, err := grpc.NewClient(grpcHost, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		return "", errors.New("Failed to get predicted move from chessapp")
	} else {
		defer conn.Close()
		client := pb.NewAiServiceClient(conn)

		bitboardsState := &pb.PredictedMoveRequest_BitboardsState{
			WhitePawns:   bitboards.WhitePawns,
			WhiteKnights: bitboards.WhiteKnights,
			WhiteBishops: bitboards.WhiteBishops,
			WhiteRooks:   bitboards.WhiteRooks,
			WhiteQueens:  bitboards.WhiteQueens,
			WhiteKings:   bitboards.WhiteKings,
			BlackPawns:   bitboards.BlackPawns,
			BlackKnights: bitboards.BlackKnights,
			BlackBishops: bitboards.BlackBishops,
			BlackRooks:   bitboards.BlackRooks,
			BlackQueens:  bitboards.BlackQueens,
			BlackKings:   bitboards.BlackKings,
		}

		predictResp, err := client.GetPredictedMove(ctx, &pb.PredictedMoveRequest{
			BitboardsState: bitboardsState,
			IsWhiteTurn:    isWhiteTurn,
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
