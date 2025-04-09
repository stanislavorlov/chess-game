import { Square } from "src/app/services/models/chess-game";
import { Side } from "../side";

export abstract class Piece {
    private _id: string;
    private _side: Side;

    constructor(piece_id: string, side: Side) {
        this._id = piece_id;
        this._side = side;
    }

    abstract validate_move(from: Square, to: Square) : boolean;
}