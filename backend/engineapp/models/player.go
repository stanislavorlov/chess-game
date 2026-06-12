package models

import "github.com/google/uuid"

type Player struct {
	ID    string
	IsBot bool
}

func NewGuestPlayer() *Player {
	return &Player{
		ID:    uuid.New().String(),
		IsBot: false,
	}
}

func NewBotPlayer() *Player {
	return &Player{
		ID:    "bot",
		IsBot: true,
	}
}

func NewAuthenticatedPlayer(id string) *Player {
	return &Player{
		ID:    id,
		IsBot: false,
	}
}
