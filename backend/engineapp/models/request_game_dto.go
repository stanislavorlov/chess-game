package models

type RequestComputerGame struct {
	Format      string `json:"format"`      // blitz, rapid, classical, bullet
	BaseTime    int    `json:"baseTime"`    // Starting time in seconds
	Increment   int    `json:"increment"`   // Increment in seconds per move
	Color       string `json:"color"`       // white, black, random
	Difficulty  string `json:"difficulty"`  // engine strength level
	StartingFEN string `json:"startingFen"` // Optional: custom starting position
}

type RequestOnlineGame struct {
	Format          string `json:"format"`          // blitz, rapid, classical, bullet
	BaseTime        int    `json:"baseTime"`        // Starting time in seconds
	Increment       int    `json:"increment"`       // Increment in seconds per move
	ColorPreference string `json:"colorPreference"` // white, black, random
	Rated           bool   `json:"rated"`           // Is the game affecting ELO?
	Culture         string `json:"culture"`         // en, es, fr, de, etc.
	OpponentID      string `json:"opponentId"`      // Optional: direct challenge
	// MinRating / MaxRating could also go here for open seeks
}
