import { PieceDto } from "src/app/services/models/chess-game-dto";
import { Side } from "../side";
import { Bishop } from "./bishop";
import { King } from "./king";
import { Knight } from "./knight";
import { Pawn } from "./pawn";
import { Queen } from "./queen";
import { Rook } from "./rook";

export class PieceFactory {
    
    static getPiece(piece: PieceDto) {
        switch (piece.abbreviation.toLowerCase()) {
            case 'wp':
                return new Pawn(piece.piece_id, Side.white);
            case 'bp':
                return new Pawn(piece.piece_id, Side.black);
            case 'wr':
                return new Rook(piece.piece_id, Side.white);
            case 'br':
                return new Rook(piece.piece_id, Side.black);
            case 'wb':
                return new Bishop(piece.piece_id, Side.white);
            case 'bb':
                return new Bishop(piece.piece_id, Side.black);
            case 'wn':
                return new Knight(piece.piece_id, Side.white);
            case 'bn':
                return new Knight(piece.piece_id, Side.black);
            case 'wq':
                return new Queen(piece.piece_id, Side.white);
            case 'bq':
                return new Queen(piece.piece_id, Side.black);
            case 'wk':
                return new King(piece.piece_id, Side.white);
            case 'bk':
                return new King(piece.piece_id, Side.black);
            default:
                throw Error('Un-recognized piece type');
        }
    }
}