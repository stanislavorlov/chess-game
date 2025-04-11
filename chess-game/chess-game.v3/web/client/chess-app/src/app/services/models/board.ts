import { Piece } from "src/app/pages/game/play/play/models/pieces/piece";
import { Square } from "./chess-game";
import { PieceFactory } from "src/app/pages/game/play/play/models/pieces/piece_factory";
import { PieceType } from "src/app/pages/game/play/play/models/pieces/piece_type";

export class Board {
    private board: (Piece | null)[][];
    private files: string[] = ['a','b','c','d','e','f','g','h'];
    private ranks: number[] = [0,1,2,3,4,5,6,7];

    constructor(squares: Square[]) {
        this.board = [];
        let that = this;

        squares.forEach(function (square: Square) {
            const [file,rank] = square.square;
            const fileIdx = that.files.indexOf(file);
            const rankIdx = that.ranks.indexOf(Number(rank));
            
            if (!that.board[fileIdx]) {
                that.board[fileIdx] = [];
            }

            if (!!square.piece) {
                that.board[fileIdx][rankIdx] = PieceFactory.getPiece('', square.piece);
            } else {
                that.board[fileIdx][rankIdx] = null;
            }
        });
    }

    isValidMove(from: Square, to: Square) : boolean {
        const [file,rank] = from.square;
        const fileIdx = this.files.indexOf(file);
        const rankIdx = this.ranks.indexOf(Number(rank));

        let piece = this.board[fileIdx][rankIdx];
        if (!!piece && piece.validateMove(from, to)) {
            // Knight
            if (piece.can_move_over) {
                return true;
            }

            const [toFile,toRank] = to.square;
            const toFileIdx = this.files.indexOf(toFile);
            const toRankIdx = this.ranks.indexOf(Number(toRank));

            // Pawn, Rook, Bishop, King, Queen
            // ToDo: iterate though the list [from:to] to check for any piece on a route
            if (piece.type == PieceType.Pawn) {
                if (rankIdx < toRankIdx) {
                    for (let step = rankIdx+1; step <= toRankIdx; step++) {
                        if (this.board[fileIdx][step] != null) {
                            return false;
                        }
                    }
                } else {
                    for (let step = rankIdx-1; step >= toRankIdx; step--) {
                        if (this.board[fileIdx][step] != null) {
                            return false;
                        }
                    }
                }
            } else if (piece.type == PieceType.Rook) {

            } else if (piece.type == PieceType.Bishop) {

            } else if (piece.type == PieceType.Queen) {

            } else if (piece.type == PieceType.King) {

            }

            return true;
        }

        return false;
    }
}