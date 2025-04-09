import { Square } from "src/app/services/models/chess-game";
import { Side } from "../side";
import { Piece } from "./piece";

export class Pawn extends Piece {

    constructor(piece_id: string, side: Side) {
        super(piece_id, side);
    }

    override validate_move(from: Square, to: Square): boolean {
        throw new Error("Method not implemented.");
    }
}