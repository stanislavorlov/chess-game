import { Cell } from "../board/ cell";
import { Side } from "../side";
import { Piece } from "./piece";
import { PieceType } from "./piece_type";

export class Knight extends Piece {
    override get can_move_over(): boolean {
        return true;
    }

    constructor(side: Side) {
        super(side, PieceType.Knight);
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

        return (absFile === 1 && absRank === 2) || (absFile === 2 && absRank === 1);
    }
}