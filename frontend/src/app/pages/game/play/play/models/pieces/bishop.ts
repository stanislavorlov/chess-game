import { Cell } from "../board/ cell";
import { Side } from "../side";
import { Piece } from "./piece";
import { PieceType } from "./piece_type";

export class Bishop extends Piece {
    
    override get can_move_over(): boolean {
        return false;
    }
    
    constructor(side: Side) {
        super(side, PieceType.Bishop);
    }

    override validateMove(from: Cell, to: Cell): boolean {
        const [delta_file, delta_rank] = this.calculateMoveDeltas(from, to);

        return delta_file == delta_rank;
    }
}