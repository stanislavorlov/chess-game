import { Cell } from "../board/ cell";
import { Side } from "../side";
import { Piece } from "./piece";
import { PieceType } from "./piece_type";

export class Knight extends Piece {
    override get can_move_over(): boolean {
        return true;
    }
    
    constructor(piece_id: string, side: Side) {
        super(piece_id, side, PieceType.Knight);
    }

    override validateMove(from: Cell, to: Cell): boolean {
        const [delta_file, delta_rank] = this.calculateMoveDeltas(from, to);
        let tuple = [Math.abs(delta_file), Math.abs(delta_rank)];

        const allowedPoints: [number, number][] = [
            [1, 2],
            [2, 1],
          ];

        return allowedPoints.some(allowed => allowed[0] === tuple[0] && allowed[1] === tuple[1]);
    }
}