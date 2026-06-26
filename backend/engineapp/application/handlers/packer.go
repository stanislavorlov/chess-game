package handlers

import (
	"fmt"
	"strings"

	"engineapp/domain/models"
)

func PackGameState(game *models.Game) uint8 {
	var state uint8
	if game.IsCheck() {
		state |= 1 // bit 0: check
	}
	if game.IsCheckmate() {
		state |= 1 << 1 // bit 1: checkmate
	}
	if game.IsStalemate() {
		state |= 1 << 2 // bit 2: stalemate
	}
	if game.IsDraw() {
		state |= 1 << 3 // bit 3: draw
	}
	if game.Turn() == "b" {
		state |= 1 << 4 // bit 4: turn (0=w, 1=b)
	}
	if game.Winner() == "b" {
		state |= 1 << 5 // bit 5: winner is black
	} else if game.Winner() == "w" {
		state |= 1 << 6 // bit 6: winner is white
	}
	return state
}

func PackFenToBytes(fen string) []byte {
	// Our agreed-upon piece dictionary mapping runes to bytes (uint8)
	pieceMap := map[rune]byte{
		'P': 1, 'N': 2, 'B': 3, 'R': 4, 'Q': 5, 'K': 6,
		'p': 7, 'n': 8, 'b': 9, 'r': 10, 'q': 11, 'k': 12,
	}

	// Initialize a buffer of exactly 34 bytes (auto-filled with zeros in Go)
	buffer := make([]byte, 34)
	parts := strings.Split(fen, " ")

	board, turn, castling, enPassant := parts[0], parts[1], parts[2], parts[3]

	// --- BYTE 0 to 31: Pack the 64 squares ---
	// Pre-allocate a slice with a capacity of 64 to avoid memory reallocations
	squares := make([]byte, 0, 64)

	for _, char := range board {
		if char >= '1' && char <= '8' {
			// Convert the rune digit into an actual integer and add empty squares
			emptyCount := int(char - '0')
			for i := 0; i < emptyCount; i++ {
				squares = append(squares, 0)
			}
		} else if char != '/' {
			// Add the mapped piece integer
			squares = append(squares, pieceMap[char])
		}
	}

	// Combine two 4-bit squares into one 8-bit byte
	for i := 0; i < 32; i++ {
		sq1 := squares[i*2]   // Square 1
		sq2 := squares[i*2+1] // Square 2
		// Shift sq1 left by 4 bits, then OR it with sq2
		buffer[i] = (sq1 << 4) | sq2
	}

	// --- BYTE 32: Pack Castling Rights ---
	var cByte byte = 0
	if strings.ContainsRune(castling, 'K') {
		cByte |= 1
	} // 0001
	if strings.ContainsRune(castling, 'Q') {
		cByte |= 1 << 1
	} // 0010
	if strings.ContainsRune(castling, 'k') {
		cByte |= 1 << 2
	} // 0100
	if strings.ContainsRune(castling, 'q') {
		cByte |= 1 << 3
	} // 1000
	buffer[32] = cByte

	// --- BYTE 33: Pack Turn and En Passant ---
	var turnBit byte = 0
	if turn == "b" {
		turnBit = 1
	}

	var epVal byte = 8 // We use 8 to represent "No En Passant target"
	if enPassant != "-" {
		// Convert file 'a'-'h' to an integer 0-7
		// enPassant[0] gets the ASCII value of the first letter
		epVal = enPassant[0] - 'a'
	}

	// Shift EP value left by 1 bit, insert turn into the lowest bit
	buffer[33] = (epVal << 1) | turnBit

	return buffer
}

func main() {
	fen := "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
	binaryPayload := PackFenToBytes(fen)

	fmt.Printf("Payload size: %d bytes\n", len(binaryPayload))
	fmt.Printf("Raw bytes: %v\n", binaryPayload)
}

// ********************* How to decode back from 34 bytes to FEN (for testing) ********************* //
/* A reverse map to easily print/draw the pieces
const REVERSE_PIECE_MAP = [
    'Empty',
    'P', 'N', 'B', 'R', 'Q', 'K',
    'p', 'n', 'b', 'r', 'q', 'k'
];

function decode34Bytes(arrayBuffer) {
    // Treat the raw buffer as an array of 8-bit unsigned integers
    const view = new Uint8Array(arrayBuffer);
    const squares = [];

    // --- Unpack Bytes 0-31: The 64 squares ---
    for (let i = 0; i < 32; i++) {
        const byte = view[i];

        // Extract the high 4 bits (shift right by 4)
        const sq1 = byte >> 4;

        // Extract the low 4 bits (bitwise AND with 1111)
        const sq2 = byte & 0x0F;

        squares.push(REVERSE_PIECE_MAP[sq1], REVERSE_PIECE_MAP[sq2]);
    }

    // --- Unpack Byte 32: Castling ---
    const cByte = view[32];
    const castling = {
        whiteKingSide:  !!(cByte & 1), // Check bit 0
        whiteQueenSide: !!(cByte & 2), // Check bit 1
        blackKingSide:  !!(cByte & 4), // Check bit 2
        blackQueenSide: !!(cByte & 8)  // Check bit 3
    };

    // --- Unpack Byte 33: Turn and En Passant ---
    const tEpByte = view[33];
    const turn = (tEpByte & 1) === 0 ? 'w' : 'b'; // Bit 0 is the turn

    const epVal = tEpByte >> 1; // Shift right to drop the turn bit
    const enPassantFile = epVal === 8 ? '-' : String.fromCharCode(97 + epVal); // 97 is 'a'

    return {
        board: squares,
        turn: turn,
        castling: castling,
        enPassant: enPassantFile
    };
}

/* Example WebSocket integration:
  socket.binaryType = "arraybuffer"; // Tell the browser to expect raw binary

  socket.onmessage = function(event) {
      if (event.data instanceof ArrayBuffer) {
          const gameState = decode34Bytes(event.data);
          console.log("Turn:", gameState.turn);
          // Render your UI using gameState.board array...
      }
  };
*/
