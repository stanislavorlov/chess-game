import { MoveFailureReason } from "../move-failure-reason";
import { Side } from "../side";

export abstract class GameEvent {
    constructor(public readonly game_id: string, public readonly event_type: string) { }
}

export class PieceMovedEvent extends GameEvent {
    constructor(game_id: string, public readonly from_: string, public readonly to: string) {
        super(game_id, 'piece-moved');
    }
}

export class PieceCapturedEvent extends GameEvent {
    constructor(game_id: string, public readonly from_: string, public readonly to: string, public readonly captured: string) {
        super(game_id, 'piece-captured');
    }
}

export class PieceMoveFailedEvent extends GameEvent {
    constructor(game_id: string, public readonly reason: MoveFailureReason, public readonly from_: string, public readonly to: string) {
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

export class KingCastledEvent extends GameEvent {
    constructor(game_id: string, public readonly side: string, public readonly king_from: string, public readonly king_to: string, public readonly rook_from: string, public readonly rook_to: string, public readonly is_kingside: boolean) {
        super(game_id, 'king-castled');
    }
}

export class SyncedStateEvent extends GameEvent {
    constructor(game_id: string, public readonly turn: Side, public readonly legal_moves: any[]) {
        super(game_id, 'synced-state');
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
            case 'king-castled':
                return new KingCastledEvent(data.game_id, data.side, data.king_from, data.king_to, data.rook_from, data.rook_to, data.is_kingside);
            case 'synced-state':
                return new SyncedStateEvent(data.game_id, Side.parse(data.turn), data.legal_moves || []);
            default:
                return null;
        }
    }
}