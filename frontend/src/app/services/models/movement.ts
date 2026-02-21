import { Piece } from "src/app/pages/game/play/play/models/pieces/piece";

export class Movement {
    public gameId: string;
    public piece: Piece;
    public from: string;
    public to: string;

    public capturedPiece: Piece | null = null;

    constructor(game_id: string, piece: Piece, from: string, to: string, capturedPiece: Piece | null = null) {
        this.gameId = game_id;
        this.piece = piece;
        this.from = from;
        this.to = to;
        this.capturedPiece = capturedPiece;
    }

    get square() {
        return `${this.from}-${this.to}`;
    }
}