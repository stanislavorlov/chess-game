package models

import "time"

type ChessGameDto struct {
	GameID     string        `json:"game_id"`
	MovesCount int           `json:"moves_count"`
	Date       time.Time     `json:"date"`
	Name       string        `json:"name"`
	State      GameStateDto  `json:"state"`
	GameFormat GameFormatDto `json:"game_format"`
	Players    PlayersDto    `json:"players"`
	Board      string        `json:"board"`
	History    string        `json:"history"`
}

type GameStateDto struct {
	Turn          string  `json:"turn"`
	Started       bool    `json:"started"`
	Finished      bool    `json:"finished"`
	CheckSide     *string `json:"check_side"`
	CheckPosition *string `json:"check_position"`
	LegalMoves    string  `json:"legal_moves"`
}

type GameFormatDto struct {
	Value              string `json:"value"`
	WhiteRemainingTime int    `json:"white_remaining_time"`
	BlackRemainingTime int    `json:"black_remaining_time"`
	MoveIncrement      int    `json:"move_increment"`
}

type PlayersDto struct {
	WhiteID string `json:"white_id"`
	BlackID string `json:"black_id"`
}
