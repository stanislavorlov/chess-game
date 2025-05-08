export class ChessGameDto {
    game_id: string;
    moves_count: number;
    date: Date;
    name: string;
    state: GameStateDto;
    game_format: GameFormatDto;
    players: PlayersDto;
    board: SquareDto[];
    history: HistoryEntryDto[];
}
export class HistoryEntryDto {
    sequence: number;
    piece: PieceDto;
    from: string;
    to: string;
}
export class GameStateDto {
    turn: string;
    started: boolean;
    finished: boolean;
}
export class GameFormatDto {
    value: string;
    remaining_time: number;
    additional_time: number;
}
export class PlayersDto {
    white_id: string;
    black_id: string;
}
export class PieceDto {
    abbreviation: string;
    piece_id: string;

    public constructor(init?:Partial<PieceDto>) {
        Object.assign(this, init);
    }
}
export class SquareDto {
    square: string;
    piece: PieceDto | null;
    color: string;
    rank: number;
}