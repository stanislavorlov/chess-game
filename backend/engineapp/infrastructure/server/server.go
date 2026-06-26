package server

import (
    // "context"
    // pb "engineapp/infrastructure/proto"
)

// ChessEngineServer implements the gRPC server (currently empty as AI logic moved to predictapp)
type ChessEngineServer struct {
}

func NewChessEngineServer() *ChessEngineServer {
	return &ChessEngineServer{}
}
