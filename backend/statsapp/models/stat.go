package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type Stat struct {
	ID          primitive.ObjectID `bson:"_id,omitempty" json:"id" swaggertype:"string"`
	GameID      string             `bson:"game_id,omitempty" json:"game_id,omitempty"`
	Type        string             `bson:"type" json:"type" binding:"required"`
	Value       float64            `bson:"value" json:"value" binding:"required"`
	LightPlayer string             `bson:"light_player,omitempty" json:"light_player,omitempty"`
	DarkPlayer  string             `bson:"dark_player,omitempty" json:"dark_player,omitempty"`
	Result      string             `bson:"result,omitempty" json:"result,omitempty"`
	Timestamp   primitive.DateTime `bson:"timestamp" json:"timestamp" swaggertype:"string"`
}
