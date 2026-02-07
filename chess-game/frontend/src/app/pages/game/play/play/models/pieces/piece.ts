import { Cell } from "../board/ cell";
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

    get abbreviation() {
        return `${this._side.value}${this._type}`.toLowerCase();
    }

    abstract get can_move_over(): boolean;

    abstract validateMove(from: Cell, to: Cell) : boolean;

    calculateMoveDeltas(from: Cell, to: Cell) {
        let delta_file = Math.abs((to.file.charCodeAt(0) - 'a'.charCodeAt(0)) - (from.file.charCodeAt(0) - 'a'.charCodeAt(0)));
        let delta_rank = Math.abs(from.rank - to.rank);

        return [delta_file, delta_rank];

        return [];
    }
}