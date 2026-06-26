package models

type GameMode string

const (
	ModeBot    GameMode = "bot"
	ModeOnline GameMode = "online"
)


type SideName string

const (
	SideNameWhite SideName = "White"
	SideNameBlack SideName = "Black"
)

type Square string

const (
	SqA1 Square = "a1"
	SqC1 Square = "c1"
	SqD1 Square = "d1"
	SqE1 Square = "e1"
	SqF1 Square = "f1"
	SqG1 Square = "g1"
	SqH1 Square = "h1"
	SqA8 Square = "a8"
	SqC8 Square = "c8"
	SqD8 Square = "d8"
	SqE8 Square = "e8"
	SqF8 Square = "f8"
	SqG8 Square = "g8"
	SqH8 Square = "h8"
)
