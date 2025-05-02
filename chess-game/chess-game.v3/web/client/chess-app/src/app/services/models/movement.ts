import { Piece } from "src/app/pages/game/play/play/models/pieces/piece";

export class Movement {
    public game_id: string;
    public piece: Piece;
    public from: string;
    public to: string;

    constructor(game_id: string, piece: Piece, from: string, to: string) {
        this.game_id = game_id;
        this.piece = piece;
        this.from = from;
        this.to = to;
    }

    get square() {
        return `${this.from}-${this.to}`;
    }
}