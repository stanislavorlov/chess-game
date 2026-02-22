import { Piece } from "src/app/pages/game/play/play/models/pieces/piece";

export class Movement {
    public gameId: string;
    public piece: Piece;
    public from: string;
    public to: string;
    public capturedPiece: Piece | null = null;
    public san: string | null = null;

    private constructor(gameId: string, piece: Piece, from: string, to: string) {
        this.gameId = gameId;
        this.piece = piece;
        this.from = from;
        this.to = to;
    }

    public static create(gameId: string, piece: Piece, from: string, to: string): Movement {
        return new Movement(gameId, piece, from, to);
    }

    public withCapturedPiece(capturedPiece: Piece): Movement {
        this.capturedPiece = capturedPiece;
        return this;
    }

    public withSan(san: string): Movement {
        this.san = san;
        return this;
    }

    get square() {
        return `${this.from}-${this.to}`;
    }
}