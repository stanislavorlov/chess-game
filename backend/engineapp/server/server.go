package server

import (
    // "context"
    // pb "engineapp/proto"
)

// ChessEngineServer implements the gRPC server (currently empty as AI logic moved to chessapp)
type ChessEngineServer struct {
}

func NewChessEngineServer() *ChessEngineServer {
	return &ChessEngineServer{}
}
