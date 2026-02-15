import { Cell } from "../board/ cell";
import { Side } from "../side";
import { Piece } from "./piece";
import { PieceType } from "./piece_type";

export class Rook extends Piece {

    override get can_move_over(): boolean {
        return false;
    }

    constructor(side: Side) {
        super(side, PieceType.Rook);
    }

    override validatePush(from: Cell, to: Cell): boolean {
        return this.commonValidate(from, to);
    }

    override validateCapture(from: Cell, to: Cell): boolean {
        return this.commonValidate(from, to);
    }

    private commonValidate(from: Cell, to: Cell): boolean {
        const [delta_file, delta_rank] = this.calculateMoveDeltas(from, to);
        return delta_file === 0 || delta_rank === 0;
    }
}