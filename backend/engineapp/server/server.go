package server

import (
	"context"

	pb "engineapp/proto"
)

type ChessEngineServer struct {
	pb.UnimplementedChessEngineServer
}

func NewChessEngineServer() *ChessEngineServer {
	return &ChessEngineServer{}
}

func (s *ChessEngineServer) ValidateMove(ctx context.Context, req *pb.MoveRequest) (*pb.MoveResponse, error) {
	// TODO: Integrate actual move validation logic
	// For now, we return a dummy response
	return &pb.MoveResponse{
		IsLegal: true,
		NewFen:  req.Fen,
		Error:   "",
	}, nil
}
