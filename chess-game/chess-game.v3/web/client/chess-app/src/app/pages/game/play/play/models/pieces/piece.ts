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
}