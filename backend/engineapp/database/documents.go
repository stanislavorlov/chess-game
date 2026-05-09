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
	Mode       string      `bson:"mode"`
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

type PlayerType int

const (
	GUEST PlayerType = iota
	REGISTERED
	COMPUTER
)

type Player struct {
	ID          string     `bson:"_id"`
	Username    string     `bson:"username"`
	Type        PlayerType `bson:"type"`
	DisplayName string     `bson:"display_name"`
	CreatedAt   time.Time  `bson:"created_at"`
}

type Profile struct {
	ID           string    `bson:"_id"`
	Email        string    `bson:"email"`
	Username     string    `bson:"username"`
	DisplayName  string    `bson:"display_name"`
	PasswordHash string    `bson:"password_hash"`
	CreatedAt    time.Time `bson:"created_at"`
	Locked       bool      `bson:"locked"`
	JoinDate     time.Time `bson:"join_date"`
	InitialLevel int       `bson:"initial_level"`
	FirstName    string    `bson:"first_name"`
	LastName     string    `bson:"last_name"`
	AvatarUrl    string    `bson:"avatar_url"`
	Bio          string    `bson:"bio"`
	Language     string    `bson:"language"`
	Country      string    `bson:"country"`
}

type Session struct {
	ID         string    `bson:"_id"`
	PlayerID   string    `bson:"player_id"`
	ProfileID  string    `bson:"profile_id"`
	Token      string    `bson:"token"`
	Host       string    `bson:"hostname"`
	Agent      string    `bson:"agent"`
	Region     string    `bson:"region"`
	TimeZoneId string    `bson:"time_zone_id"`
	CreatedAt  time.Time `bson:"created_at"`
	ExpiresAt  time.Time `bson:"expires_at"`
}

type Rating struct {
	ID         string    `bson:"_id"`
	PlayerID   string    `bson:"player_id"`
	ProfileID  string    `bson:"profile_id"`
	GameFormat string    `bson:"game_format"` // e.g. "bullet", "blitz", "rapid", "classical"
	Elo        int       `bson:"elo"`         // ~1000–3000
	Deviation  int       `bson:"deviation"`   // 30–350, how uncertain we are about a player’s rating, more games -> bigger, less - slower
	UpdatedAt  time.Time `bson:"updated_at"`
}

type Stats struct {
	ID           string    `bson:"_id"`
	PlayerID     string    `bson:"player_id"`
	ProfileID    string    `bson:"profile_id"`
	GameFormat   string    `bson:"game_format"` // e.g. "bullet", "blitz", "rapid", "classical"
	GamesPlayed  int       `bson:"games_played"`
	Wins         int       `bson:"wins"`
	Losses       int       `bson:"losses"`
	Draws        int       `bson:"draws"`
	UpdatedAt    time.Time `bson:"updated_at"`
	WinStreak    int       `bson:"win_streak"`
	PlayedStreak int       `bson:"played_streak"`
}

type MatchingQueue struct {
	ID              string    `bson:"_id"`
	PlayerID        string    `bson:"player_id"`
	ProfileID       string    `bson:"profile_id"`
	GameFormat      string    `bson:"game_format"`      // e.g. "bullet", "blitz", "rapid", "classical"
	BaseTime        int       `bson:"base_time"`        // Starting time in seconds
	Increment       int       `bson:"increment"`        // Increment in seconds per move
	ColorPreference string    `bson:"color_preference"` // white, black, random
	Rated           bool      `bson:"rated"`            // Is the game affecting ELO?
	Culture         string    `bson:"culture"`          // en, es, fr, de, etc.
	OpponentID      string    `bson:"opponent_id"`      // Optional: direct challenge
	Region          string    `bson:"region"`
	RD              int       `bson:"rd"`
	Ping            int       `bson:"ping"`
	Ranking         int       `bson:"ranking"`
	CreatedAt       time.Time `bson:"created_at"`
	ExpiresAt       time.Time `bson:"expires_at"`
	Status          string    `bson:"status"`          // open, matched, cancelled
	MatchedWithID   string    `bson:"matched_with_id"` // PlayerID of the matched opponent
}
