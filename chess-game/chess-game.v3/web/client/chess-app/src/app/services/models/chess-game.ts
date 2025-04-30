export class ChessGame {
    game_id: string;
    moves_count: number;
    date: Date;
    name: string;
    state: GameState;
    game_format: GameFormat;
    players: Players;
    board: Square[];
}
export class GameState {
    turn: string;
    started: boolean;
    finished: boolean;
}
export class GameFormat {
    value: string;
    remaining_time: number;
    additional_time: number;
}
export class Players {
    white_id: string;
    black_id: string;
}
export class Piece {
    abbreviation: string;
    piece_id: string;

    public constructor(init?:Partial<Piece>) {
        Object.assign(this, init);
    }
}
export class Square {
    square: string;
    piece: Piece | null;
    color: string;
    rank: number;
}