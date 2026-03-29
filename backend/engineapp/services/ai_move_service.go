package services

import (
	"context"
	"errors"
	"log"
	"os"

	pb "engineapp/proto"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func PredictMove(ctx context.Context, gameID string, bitboards []uint64) (string, error) {
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

		var bitboardsState *pb.PredictedMoveRequest_BitboardsState
		if len(bitboards) >= 12 {
			bitboardsState = &pb.PredictedMoveRequest_BitboardsState{
				WhitePawns:   bitboards[0],
				WhiteKnights: bitboards[1],
				WhiteBishops: bitboards[2],
				WhiteRooks:   bitboards[3],
				WhiteQueens:  bitboards[4],
				WhiteKings:   bitboards[5],
				BlackPawns:   bitboards[6],
				BlackKnights: bitboards[7],
				BlackBishops: bitboards[8],
				BlackRooks:   bitboards[9],
				BlackQueens:  bitboards[10],
				BlackKings:   bitboards[11],
			}
		}

		predictResp, err := client.GetPredictedMove(ctx, &pb.PredictedMoveRequest{
			BitboardsState: bitboardsState,
			IsWhiteTurn:    true,
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
