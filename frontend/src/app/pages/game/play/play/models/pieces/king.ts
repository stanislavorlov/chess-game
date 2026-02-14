import { Cell } from "../board/ cell";
import { Side } from "../side";
import { Piece } from "./piece";
import { PieceType } from "./piece_type";

export class King extends Piece {
    
    override get can_move_over(): boolean {
        return false;
    }
    
    constructor(side: Side) {
        super(side, PieceType.King);
    }

    override validateMove(from: Cell, to: Cell): boolean {
        const [delta_file, delta_rank] = this.calculateMoveDeltas(from, to);

        return Math.abs(delta_file) <= 1 && Math.abs(delta_rank) <= 1;
    }
}