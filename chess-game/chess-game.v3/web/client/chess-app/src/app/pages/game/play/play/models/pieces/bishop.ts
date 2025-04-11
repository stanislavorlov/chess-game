import { Square } from "src/app/services/models/chess-game";
import { Side } from "../side";
import { Piece } from "./piece";
import { PieceType } from "./piece_type";

export class Bishop extends Piece {
    
    override get can_move_over(): boolean {
        return false;
    }
    
    constructor(piece_id: string, side: Side) {
        super(piece_id, side, PieceType.Bishop);
    }

    override validateMove(from: Square, to: Square): boolean {
        const [from_file, from_rank] = from.square;
        const [to_file, to_rank] = to.square;

        let delta_file = Math.abs((to_file.charCodeAt(0) - 'a'.charCodeAt(0)) - (from_file.charCodeAt(0) - 'a'.charCodeAt(0)));
        let delta_rank = Math.abs(parseInt(from_rank) - parseInt(to_rank));

        return delta_file == delta_rank;
    }
}