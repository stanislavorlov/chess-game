package database

import "time"

type GameState struct {
	ID         string    `bson:"_id"`
	GameStatus string    `bson:"game_status"`
	CreatedAt  time.Time `bson:"created_at"`
	StartedAt  time.Time `bson:"started_at"`
	FinishedAt time.Time `bson:"finished_at"`
}

type GameHistory struct {
	ID       string `bson:"_id"`
	GameID   string `bson:"game_id"`
	UciMove  string `bson:"uci_move"` // e.g. "e2e4"
	Bitboard uint64 `bson:"bitboard"`
	Sequence int    `bson:"sequence"`
}
