package health

import (
	"encoding/json"
	"net/http"
)

type HealthResponse struct {
	Status  string `json:"status"`
	Service string `json:"service"`
}

// Check returns the health status of the service.
// @Summary Check service health
// @Description returns the health status of the engineapp service
// @Tags health
// @Produce json
// @Success 200 {object} HealthResponse
// @Router /health/live [get]
func Check(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	response := HealthResponse{Status: "ok", Service: "engineapp"}
	json.NewEncoder(w).Encode(response)
}
