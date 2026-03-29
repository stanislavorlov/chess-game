package database

import "time"

type GameFormat struct {
	Format    string `bson:"format"`
	Minutes   int    `bson:"minutes"`
	Increment int    `bson:"increment"`
}

type GamePlayers struct {
	WhitePlayerId string `bson:"white_player_id"`
	BlackPlayerId string `bson:"black_player_id"`
}

type GameState struct {
	ID          string      `bson:"_id"`
	GameStatus  string      `bson:"game_status"`
	CreatedAt   time.Time   `bson:"created_at"`
	StartedAt   time.Time   `bson:"started_at"`
	FinishedAt  time.Time   `bson:"finished_at"`
	Result      string      `bson:"result"`
	GameFormat  GameFormat  `bson:"game_format"`
	GamePlayers GamePlayers `bson:"game_players"`
}

type GameHistory struct {
	ID         string        `bson:"_id"`
	GameID     string        `bson:"game_id"`
	SanMove    string        `bson:"san_move"` // e.g. "Nf3 Nc6"
	OccurredAt time.Time     `bson:"occurred_at"`
	Duration   time.Duration `bson:"duration_ns"`
	Sequence   int           `bson:"sequence"`  // ToDo: make auto-increment
	BoardFen   string        `bson:"board_fen"` // e.g. rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2
}
