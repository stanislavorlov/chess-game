import { Square } from "src/app/services/models/chess-game";
import { Side } from "../side";
import { PieceType } from "./piece_type";

export abstract class Piece {
    private _id: string;
    private _side: Side;
    private _type: PieceType;

    constructor(piece_id: string, side: Side, type: PieceType) {
        this._id = piece_id;
        this._side = side;
        this._type = type;
    }

    get id() {
        return this._id;
    }

    get side() {
        return this._side;
    }

    get type() {
        return this._type;
    }

    abstract get can_move_over(): boolean;

    abstract validateMove(from: Square, to: Square) : boolean;

    calculateMoveDeltas(from: Square, to: Square) {
        const [from_file, from_rank] = from.square;
        const [to_file, to_rank] = to.square;

        let delta_file = Math.abs((to_file.charCodeAt(0) - 'a'.charCodeAt(0)) - (from_file.charCodeAt(0) - 'a'.charCodeAt(0)));
        let delta_rank = Math.abs(parseInt(from_rank) - parseInt(to_rank));

        return [delta_file, delta_rank];
    }
}