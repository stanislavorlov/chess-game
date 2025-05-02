import { Cell } from "../board/ cell";
import { Side } from "../side";
import { Piece } from "./piece";
import { PieceType } from "./piece_type";

export class King extends Piece {
    
    override get can_move_over(): boolean {
        return false;
    }
    
    constructor(piece_id: string, side: Side) {
        super(piece_id, side, PieceType.King);
    }

    override validateMove(from: Cell, to: Cell): boolean {
        const [delta_file, delta_rank] = this.calculateMoveDeltas(from, to);

        return Math.abs(delta_file - delta_rank) == 1;
    }
}