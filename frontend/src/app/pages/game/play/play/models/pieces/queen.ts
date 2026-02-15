import { Cell } from "../board/ cell";
import { Side } from "../side";
import { Piece } from "./piece";
import { PieceType } from "./piece_type";

export class Queen extends Piece {

    override get can_move_over(): boolean {
        return false;
    }

    constructor(side: Side) {
        super(side, PieceType.Queen);
    }

    override validatePush(from: Cell, to: Cell): boolean {
        return this.commonValidate(from, to);
    }

    override validateCapture(from: Cell, to: Cell): boolean {
        return this.commonValidate(from, to);
    }

    private commonValidate(from: Cell, to: Cell): boolean {
        const [delta_file, delta_rank] = this.calculateMoveDeltas(from, to);
        const absFile = Math.abs(delta_file);
        const absRank = Math.abs(delta_rank);

        // rook-like or bishop-like
        return (absFile === 0 || absRank === 0) || (absFile === absRank);
    }
}