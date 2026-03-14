package models

type Side string

const (
	White Side = "w"
	Black Side = "b"
)

func ToSide(side string) Side {
	if side == "w" {
		return White
	}
	return Black
}
