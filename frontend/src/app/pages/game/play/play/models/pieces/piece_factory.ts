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
                return new Pawn(Side.white);
            case 'bp':
                return new Pawn(Side.black);
            case 'wr':
                return new Rook(Side.white);
            case 'br':
                return new Rook(Side.black);
            case 'wb':
                return new Bishop(Side.white);
            case 'bb':
                return new Bishop(Side.black);
            case 'wn':
                return new Knight(Side.white);
            case 'bn':
                return new Knight(Side.black);
            case 'wq':
                return new Queen(Side.white);
            case 'bq':
                return new Queen(Side.black);
            case 'wk':
                return new King(Side.white);
            case 'bk':
                return new King(Side.black);
            default:
                throw Error('Un-recognized piece type');
        }
    }
}