import { Square } from "src/app/services/models/chess-game";
import { Side } from "../side";
import { Piece } from "./piece";
import { PieceType } from "./piece_type";

export class Rook extends Piece {
    
    override get can_move_over(): boolean {
        return false;
    }

    constructor(piece_id: string, side: Side) {
        super(piece_id, side, PieceType.Rook);
    }

    override validateMove(from: Square, to: Square): boolean {
        const [delta_file, delta_rank] = this.calculateMoveDeltas(from, to);

        return delta_file == 0 || delta_rank == 0;
    }
}