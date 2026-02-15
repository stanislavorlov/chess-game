import { Cell } from "../board/ cell";
import { Side } from "../side";
import { Piece } from "./piece";
import { PieceType } from "./piece_type";

export class Pawn extends Piece {

    override get can_move_over(): boolean {
        return false;
    }

    constructor(side: Side) {
        super(side, PieceType.Pawn);
    }

    override validatePush(from: Cell, to: Cell): boolean {
        const [delta_file, delta_rank] = this.calculateMoveDeltas(from, to);

        if (this.side === Side.white) {
            // White pawns move up (+Rank)
            return delta_file === 0 && (delta_rank === 1 || (delta_rank === 2 && from.rank === 2));
        } else {
            // Black pawns move down (-Rank)
            return delta_file === 0 && (delta_rank === -1 || (delta_rank === -2 && from.rank === 7));
        }
    }

    override validateCapture(from: Cell, to: Cell): boolean {
        const [delta_file, delta_rank] = this.calculateMoveDeltas(from, to);

        if (this.side === Side.white) {
            return Math.abs(delta_file) === 1 && delta_rank === 1;
        } else {
            return Math.abs(delta_file) === 1 && delta_rank === -1;
        }
    }
}