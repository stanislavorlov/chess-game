package controllers

import (
	"context"
	"net/http"
	"time"

	"statsapp/database"
	"statsapp/models"

	"github.com/gin-gonic/gin"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

// CreateStat godoc
// @Summary      Create a new stat
// @Description  Create a stat entry in the database
// @Tags         stats
// @Accept       json
// @Produce      json
// @Param        stat body models.Stat true "Stat Data"
// @Success      201  {object}  models.Stat
// @Router       /stats [post]
func CreateStat(c *gin.Context) {
	var stat models.Stat
	if err := c.ShouldBindJSON(&stat); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	stat.Timestamp = primitive.NewDateTimeFromTime(time.Now())

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	result, err := database.StatCollection.InsertOne(ctx, stat)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create stat"})
		return
	}

	stat.ID = result.InsertedID.(primitive.ObjectID)
	c.JSON(http.StatusCreated, stat)
}

// GetStats godoc
// @Summary      Get all stats
// @Description  Fetch all stats from the database
// @Tags         stats
// @Produce      json
// @Success      200  {array}   models.Stat
// @Router       /stats [get]
func GetStats(c *gin.Context) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	cursor, err := database.StatCollection.Find(ctx, bson.M{})
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to fetch stats"})
		return
	}
	defer cursor.Close(ctx)

	var stats []models.Stat
	if err = cursor.All(ctx, &stats); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to decode stats"})
		return
	}

	if stats == nil {
		stats = []models.Stat{}
	}

	c.JSON(http.StatusOK, stats)
}

type PlayerMatchDto struct {
	ID          primitive.ObjectID `json:"id"`
	Type        string             `json:"type"`
	Value       float64            `json:"value"`
	LightPlayer string             `json:"light_player"`
	DarkPlayer  string             `json:"dark_player"`
	Result      string             `json:"result"`
	Timestamp   primitive.DateTime `json:"timestamp"`
	Outcome     string             `json:"outcome"` // "win", "loss", "draw"
}

// GetPlayerStats godoc
// @Summary      Get player stats
// @Description  Fetch recent matches and outcomes for a player by ID
// @Tags         stats
// @Produce      json
// @Param        playerId path string true "Player ID"
// @Success      200  {array}   PlayerMatchDto
// @Router       /stats/player/{playerId} [get]
func GetPlayerStats(c *gin.Context) {
	playerId := c.Param("playerId")
	if playerId == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "playerId is required"})
		return
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	filter := bson.M{
		"$or": []bson.M{
			{"light_player": playerId},
			{"dark_player": playerId},
		},
	}

	cursor, err := database.StatCollection.Find(ctx, filter)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to fetch stats"})
		return
	}
	defer cursor.Close(ctx)

	var stats []models.Stat
	if err = cursor.All(ctx, &stats); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to decode stats"})
		return
	}

	var matches []PlayerMatchDto
	for _, s := range stats {
		outcome := "draw"
		if s.Result != "" {
			if s.Result == playerId {
				outcome = "win"
			} else {
				outcome = "loss"
			}
		}

		matches = append(matches, PlayerMatchDto{
			ID:          s.ID,
			Type:        s.Type,
			Value:       s.Value,
			LightPlayer: s.LightPlayer,
			DarkPlayer:  s.DarkPlayer,
			Result:      s.Result,
			Timestamp:   s.Timestamp,
			Outcome:     outcome,
		})
	}

	if matches == nil {
		matches = []PlayerMatchDto{}
	}

	c.JSON(http.StatusOK, matches)
}

