package ws

import (
	"log"
	"net/http"
	"strings"

	"github.com/gorilla/websocket"
)

var upgrader = websocket.Upgrader{
	ReadBufferSize:  1024,
	WriteBufferSize: 1024,
	CheckOrigin: func(r *http.Request) bool {
		return true // Allow all connections for now
	},
}

type Client struct {
	conn *websocket.Conn
	send chan []byte
}

var clients = make(map[*Client]bool)

func HandleConnections(w http.ResponseWriter, r *http.Request) {
	// Extract game_id from path: /ws/{game_id}
	path := r.URL.Path
	gameID := strings.TrimPrefix(path, "/ws/")

	if gameID == "" || gameID == "/" {
		http.Error(w, "Game ID is required", http.StatusBadRequest)
		return
	}

	ws, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Printf("Error upgrading to websocket: %v", err)
		return
	}
	defer ws.Close()

	client := &Client{conn: ws, send: make(chan []byte, 256)}
	clients[client] = true
	log.Printf("New WebSocket client connected to game %s", gameID)

	for {
		_, message, err := ws.ReadMessage()
		if err != nil {
			log.Printf("WebSocket client disconnected or error: %v", err)
			delete(clients, client)
			break
		}

		log.Printf("Received message: %s", message)

		// Echo for now, can be replaced by actual logic later
		if err := ws.WriteMessage(websocket.TextMessage, message); err != nil {
			log.Printf("Error writing message: %v", err)
			delete(clients, client)
			break
		}
	}
}
