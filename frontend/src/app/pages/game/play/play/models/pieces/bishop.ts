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

    override validatePush(from: Cell, to: Cell): boolean {
        return this.commonValidate(from, to);
    }

    override validateCapture(from: Cell, to: Cell): boolean {
        return this.commonValidate(from, to);
    }

    private commonValidate(from: Cell, to: Cell): boolean {
        const [delta_file, delta_rank] = this.calculateMoveDeltas(from, to);
        return Math.abs(delta_file) === Math.abs(delta_rank);
    }
}