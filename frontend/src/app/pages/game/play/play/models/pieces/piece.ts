import { Cell } from "../board/ cell";
import { Side } from "../side";
import { PieceType } from "./piece_type";

export abstract class Piece {
    private _side: Side;
    private _type: PieceType;
    private _moved: boolean;

    constructor(side: Side, type: PieceType) {
        this._side = side;
        this._type = type;
        this._moved = false;
    }

    get id() {
        return `${this._side.value}${this._type}`;
    }

    get moved() {
        return this._moved;
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

    /**
     * Validates if the move is geometrically possible as a "push" (to an empty square).
     */
    abstract validatePush(from: Cell, to: Cell): boolean;

    /**
     * Validates if the move is geometrically possible as a "capture" (to an occupied square).
     */
    abstract validateCapture(from: Cell, to: Cell): boolean;

    calculateMoveDeltas(from: Cell, to: Cell) {
        let delta_file = (to.file.charCodeAt(0) - 'a'.charCodeAt(0)) - (from.file.charCodeAt(0) - 'a'.charCodeAt(0));
        let delta_rank = to.rank - from.rank;

        return [delta_file, delta_rank];
    }

    markMoved() {
        this._moved = true;
    }
}