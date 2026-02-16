export abstract class GameEvent {
    constructor(public readonly game_id: string, public readonly event_type: string) { }
}

export class PieceMovedEvent extends GameEvent {
    constructor(game_id: string, public readonly from: string, public readonly to: string) {
        super(game_id, 'piece-moved');
    }
}

export class PieceCapturedEvent extends GameEvent {
    constructor(game_id: string, public readonly from: string, public readonly to: string, public readonly captured: string) {
        super(game_id, 'piece-captured');
    }
}

export class PieceMoveFailedEvent extends GameEvent {
    constructor(game_id: string, public readonly reason: string, public readonly from: string, public readonly to: string) {
        super(game_id, 'piece-move-failed');
    }
}

export class KingCheckedEvent extends GameEvent {
    constructor(game_id: string, public readonly side: string, public readonly position: string) {
        super(game_id, 'king-checked');
    }
}

export class KingCheckmatedEvent extends GameEvent {
    constructor(game_id: string, public readonly side: string, public readonly position: string) {
        super(game_id, 'king-checkmated');
    }
}

export class GameEventFactory {
    static fromRaw(data: any): GameEvent | null {
        switch (data.event_type) {
            case 'piece-moved':
                return new PieceMovedEvent(data.game_id, data.from, data.to);
            case 'piece-captured':
                return new PieceCapturedEvent(data.game_id, data.from, data.to, data.captured);
            case 'piece-move-failed':
                return new PieceMoveFailedEvent(data.game_id, data.reason, data.from_, data.to);
            case 'king-checked':
                return new KingCheckedEvent(data.game_id, data.side, data.position);
            case 'king-checkmated':
                return new KingCheckmatedEvent(data.game_id, data.side, data.position);
            default:
                return null;
        }
    }
}