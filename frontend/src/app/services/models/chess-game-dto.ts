export class ChessGameDto {
    game_id: string;
    moves_count: number;
    date: Date;
    name: string;
    state: GameStateDto;
    game_format: GameFormatDto;
    players: PlayersDto;
    board: string;
    history: string;
}

export class GameStateDto {
    turn: string;
    started: boolean;
    finished: boolean;
    check_side: string | null;
    check_position: string | null;
    legal_moves: string;
}

export class GameFormatDto {
    value: string;
    white_remaining_time: number;
    black_remaining_time: number;
    move_increment: number;
}

export class PlayersDto {
    white_id: string;
    black_id: string;
}

export class PieceDto {
    abbreviation: string;
    moved: boolean;

    public constructor(init?: Partial<PieceDto>) {
        Object.assign(this, init);
    }
}