package database

import "time"

type GameFormat struct {
	Name            string `bson:"name"`
	Minutes         int    `bson:"minutes"`
	MoveIncrementMs int    `bson:"move_increment_ms"`
}

type GamePlayers struct {
	LightPlayerId string `bson:"light_player_id"`
	DarkPlayerId  string `bson:"dark_player_id"`
}

type GameResult struct {
	Winner string `bson:"winner"`
	Reason string `bson:"reason"`
}

type GameState struct {
	ID         string      `bson:"_id"`
	Status     string      `bson:"status"`
	CreatedAt  time.Time   `bson:"created_at"`
	StartedAt  time.Time   `bson:"started_at"`
	FinishedAt time.Time   `bson:"finished_at"`
	Result     GameResult  `bson:"result"`
	Format     GameFormat  `bson:"format"`
	Players    GamePlayers `bson:"players"`
}

type GameHistory struct {
	ID              string        `bson:"_id"`
	GameID          string        `bson:"game_id"`
	SanMove         string        `bson:"san_move"` // e.g. "Nf3 Nc6"
	OccurredAt      time.Time     `bson:"occurred_at"`
	Duration        time.Duration `bson:"duration_ns"`
	LightRemainigMs int64         `bson:"light_remainig_ms"`
	DarkRemainigMs  int64         `bson:"dark_remainig_ms"`
	Sequence        int           `bson:"sequence"`  // ToDo: make auto-increment
	BoardFen        string        `bson:"board_fen"` // e.g. rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2
}
