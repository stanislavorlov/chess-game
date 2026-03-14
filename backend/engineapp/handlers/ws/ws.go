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

func HandleConnections(moveHandler func(gameID string, message []byte) []byte) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		// Extract game_id from path: /ws/{game_id}
		path := r.URL.Path
		gameID := strings.TrimPrefix(path, "/ws/")

		if gameID == "" || gameID == "/" {
			http.Error(w, "Game ID is required", http.StatusBadRequest)
			return
		}

		wsConn, err := upgrader.Upgrade(w, r, nil)
		if err != nil {
			log.Printf("Error upgrading to websocket: %v", err)
			return
		}
		defer wsConn.Close()

		client := &Client{conn: wsConn, send: make(chan []byte, 256)}
		clients[client] = true
		log.Printf("New WebSocket client connected to game %s", gameID)

		for {
			_, message, err := wsConn.ReadMessage()
			if err != nil {
				log.Printf("WebSocket client disconnected or error: %v", err)
				delete(clients, client)
				break
			}

			// Route message to appropriate handler
			responseBytes := moveHandler(gameID, message)

			if len(responseBytes) > 0 {
				if err := client.conn.WriteMessage(websocket.TextMessage, responseBytes); err != nil {
					log.Printf("Error writing move response: %v", err)
					// Usually client disconnections are handled by the main read loop
				}
			}
		}
	}
}
