export class Movement {
    public piece: string;
    public from: string;
    public to: string;

    constructor(piece: string, from: string, to: string) {
        this.piece = piece;
        this.from = from;
        this.to = to;
    }
}