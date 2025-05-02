import { Piece } from "src/app/pages/game/play/play/models/pieces/piece";

export class Movement {
    public piece: Piece;
    public from: string;
    public to: string;

    constructor(piece: Piece, from: string, to: string) {
        this.piece = piece;
        this.from = from;
        this.to = to;
    }

    get square() {
        return `${this.from}-${this.to}`;
    }
}