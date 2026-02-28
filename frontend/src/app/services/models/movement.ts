import { Piece } from "src/app/pages/game/play/play/models/pieces/piece";

export abstract class Movement {
    public gameId: string;

    protected constructor(gameId: string) {
        this.gameId = gameId;
    }

    public abstract get displayValue(): string;
}

export class SquareMovement extends Movement {
    public piece: Piece;
    public from: string;
    public to: string;
    public capturedPiece: Piece | null = null;

    private constructor(gameId: string, piece: Piece, from: string, to: string) {
        super(gameId);
        this.piece = piece;
        this.from = from;
        this.to = to;
    }

    public static create(gameId: string, piece: Piece, from: string, to: string): SquareMovement {
        return new SquareMovement(gameId, piece, from, to);
    }

    public withCapturedPiece(capturedPiece: Piece): SquareMovement {
        this.capturedPiece = capturedPiece;
        return this;
    }

    get square() {
        return `${this.from}-${this.to}`;
    }

    public override get displayValue(): string {
        return this.square;
    }
}

export class SanMovement extends Movement {
    public san: string;

    constructor(gameId: string, san: string) {
        super(gameId);
        this.san = san;
    }

    public override get displayValue(): string {
        return this.san;
    }
}