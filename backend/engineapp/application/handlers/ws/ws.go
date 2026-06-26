package ws

import (
	"log"
	"net/http"
	"strings"
	"sync"

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
	mu   sync.Mutex
}

var (
	clients   = make(map[string]map[*Client]bool)
	clientsMu sync.Mutex
)

func HandleConnections(
	moveHandler func(gameID string, message []byte, send func([]byte), broadcast func([]byte)),
	connectHandler func(gameID string, send func([]byte), broadcast func([]byte)),
) http.HandlerFunc {
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

		clientsMu.Lock()
		if _, ok := clients[gameID]; !ok {
			clients[gameID] = make(map[*Client]bool)
		}
		clients[gameID][client] = true
		clientsMu.Unlock()

		log.Printf("New WebSocket client connected to game %s", gameID)

		sendMsg := func(msg []byte) {
			client.mu.Lock()
			defer client.mu.Unlock()
			if err := client.conn.WriteMessage(websocket.TextMessage, msg); err != nil {
				log.Printf("Error writing socket message: %v", err)
			}
		}

		broadcastMsg := func(msg []byte) {
			clientsMu.Lock()
			defer clientsMu.Unlock()
			for c := range clients[gameID] {
				c.mu.Lock()
				if err := c.conn.WriteMessage(websocket.TextMessage, msg); err != nil {
					log.Printf("Error broadcasting socket message: %v", err)
				}
				c.mu.Unlock()
			}
		}

		if connectHandler != nil {
			connectHandler(gameID, sendMsg, broadcastMsg)
		}

		for {
			_, message, err := wsConn.ReadMessage()
			if err != nil {
				log.Printf("WebSocket client disconnected or error: %v", err)
				clientsMu.Lock()
				delete(clients[gameID], client)
				if len(clients[gameID]) == 0 {
					delete(clients, gameID)
				}
				clientsMu.Unlock()
				break
			}

			// Route message to appropriate handler
			moveHandler(gameID, message, sendMsg, broadcastMsg)
		}
	}
}
