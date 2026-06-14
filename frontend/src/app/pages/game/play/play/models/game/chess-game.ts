import { Board } from "src/app/pages/game/play/play/models/board/board";
import { Movement, SquareMovement } from "src/app/services/models/movement";
import { Cell } from "../board/ cell";
import { Side } from "../side";
import { KingCastledEvent } from "../events/game-event";
import { PieceType } from "../pieces/piece_type";

export class ChessGame {

    private _id: string;
    private _name: string;
    private _format: GameFormat;
    private _board: Board;
    private _whiteTimer: number;
    private _blackTimer: number;
    private _turn: Side;
    private _checkSide: Side | null = null;
    private _checkPosition: string | null = null;
    private _selectableSquares: Set<string> = new Set();

    public history: Movement[];

    constructor(id: string, name: string, format: GameFormat, board: Board, turn: Side) {
        this._id = id;
        this._name = name;
        this._format = format;
        this._board = board;
        this.history = [];
        this._whiteTimer = format.white_remainig;
        this._blackTimer = format.black_remainig;
        this._turn = turn;
    }

    public setCheck(side: Side | null, position: string | null) {
        this._checkSide = side;
        this._checkPosition = position;

        this._board.cells.forEach(cell => {
            cell.checked = !cell.isHeader && !!this._checkPosition && cell.id === this._checkPosition.toLowerCase();
        });
    }

    public clearCheck() {
        this._checkSide = null;
        this._checkPosition = null;

        this._board.cells.forEach(cell => {
            cell.checked = false;
        });
    }

    get checkSide() {
        return this._checkSide;
    }

    get checkPosition() {
        return this._checkPosition;
    }

    get id() {
        return this._id;
    }

    get name() {
        return this._name;
    }

    set name(value: string) {
        this._name = value;
    }

    get board() {
        return this._board;
    }

    get format() {
        return this._format;
    }

    get whiteTimer() {
        return this._whiteTimer;
    }

    get blackTimer() {
        return this._blackTimer;
    }

    get turn() {
        return this._turn;
    }

    public movePiece(from_: Cell, to: Cell) {
        const piece = this._board.getPiece(from_);
        const isTurnFollowed = piece?.side?.value == this._turn.value;
        const isValidMove = this._board.isValidMove(from_, to);
        const isCastleMove = this._board.isCastlingMove(from_, to);

        if (isValidMove && isTurnFollowed) {
            const capturedPiece = this._board.getPiece(to);

            this._board.movePiece(from_, to);

            if (piece) {
                const entry = SquareMovement.create(this.id, piece, from_.id, to.id)
                if (!!capturedPiece) {
                    entry.withCapturedPiece(capturedPiece);
                }
                this.history.push(entry);
            }

            this.switchTurn();
            return true;
        } else if (isCastleMove && isTurnFollowed) {
            const fileDiff = to.file.charCodeAt(0) - from_.file.charCodeAt(0);
            let leftCastle = fileDiff < 0;

            const rookFrom = leftCastle ? this._board.getCell(`a${from_.rank}`) : this._board.getCell(`h${from_.rank}`);
            const rookTo = leftCastle ? this._board.getCell(`d${from_.rank}`) : this._board.getCell(`f${from_.rank}`);

            if (rookFrom && rookTo) {
                this._board.movePiece(from_, to);
                this._board.movePiece(rookFrom, rookTo);

                // Record king's move on castling, rook's move is implicit in the move entry
                if (piece) {
                    const entry = SquareMovement.create(this.id, piece, from_.id, to.id);
                    this.history.push(entry);
                }

                this.switchTurn();
                return true;
            }
        } else {
            console.log(`Invalid move. Valid move: ${isValidMove}, castle move: ${isCastleMove}, turn followed: ${isTurnFollowed}`);
        }

        return false;
    }

    public castleKing(event: KingCastledEvent) {
        console.log(`Castling king for ${event.side} from ${event.king_from} to ${event.king_to}, rook from ${event.rook_from} to ${event.rook_to}, kingside: ${event.is_kingside}`);
        const kingFrom = this._board.getCell(event.king_from);
        const kingTo = this._board.getCell(event.king_to);
        const rookFrom = this._board.getCell(event.rook_from);
        const rookTo = this._board.getCell(event.rook_to);

        if (kingFrom && kingTo && rookFrom && rookTo) {
            const side = Side.parse(event.side);

            // Only move pieces if they aren't already in their target positions
            // This prevents double-moving pieces for the player who initiated the move locally
            const kingAtFrom = this._board.getPiece(kingFrom);
            if (kingAtFrom && kingAtFrom.type === PieceType.King) {
                this._board.movePiece(kingFrom, kingTo);
                this._board.movePiece(rookFrom, rookTo);

                // Record move in history if not already there
                const lastHistory = this.history.length > 0 ? this.history[this.history.length - 1] : null;
                const isAlreadyInHistory = lastHistory instanceof SquareMovement && lastHistory.from === kingFrom.id && lastHistory.to === kingTo.id;

                if (!isAlreadyInHistory) {
                    const piece = this._board.getPiece(kingTo);
                    if (piece) {
                        const entry = SquareMovement.create(this.id, piece, kingFrom.id, kingTo.id);
                        this.history.push(entry);
                    }
                }
            }

            // Only switch turn if it's currently the turn of the side that castled
            // If the turn was already switched locally, this._turn.value will be the other side
            if (this._turn.value === side.value) {
                this.switchTurn();
            }
        }
    }

    public rollbackMove() {
        const lastMove = this.history.pop();
        if (lastMove instanceof SquareMovement) {
            // Revert the main piece
            this._board.revertMove(lastMove.from, lastMove.to, lastMove.capturedPiece);

            // Revert rook if this was a castling move (King moving 2 squares horizontally)
            if (lastMove.piece.type === PieceType.King && Math.abs(lastMove.to.charCodeAt(0) - lastMove.from.charCodeAt(0)) === 2) {
                const isKingside = (lastMove.to.charCodeAt(0) - lastMove.from.charCodeAt(0)) > 0;
                const rank = lastMove.from.charAt(1);
                
                // The rook was moved to `rookToStr` from `rookFromStr`
                const rookFromStr = (isKingside ? 'h' : 'a') + rank;
                const rookToStr = (isKingside ? 'f' : 'd') + rank;
                
                // We use revertMove to move it back
                this._board.revertMove(rookFromStr, rookToStr, null);
            }

            this.switchTurn();
        }
    }

    public timerTick() {
        if (this._turn == Side.white) {
            this._whiteTimer -= 1;
        } else {
            this._blackTimer -= 1;
        }
    }

    public syncState(turn: Side, legal_moves?: string) {
        this._turn = turn;
        if (legal_moves) {
            // legal_moves is "e2e4 e7e5..."
            const moveList = legal_moves.split(',').filter(m => m.length >= 4);
            this._selectableSquares = new Set(moveList.map(m => m.substring(0, 2)));
        }
    }

    public isSelectable(square: Cell): boolean {
        return this._selectableSquares.has(square.id);
    }

    private switchTurn() {
        this._turn = (this._turn == Side.black) ? Side.white : Side.black;
    }

    public getCapturedPieces(side: Side): string[] {
        return this._board.getCapturedPieces(side);
    }
}

export class GameInformation {

    private _name: string;
    private _format: string;
    private _date: Date;

    constructor(name: string, format: string, game_date: Date) {
        this._name = name;
        this._format = format;
        this._date = game_date;
    }

}

export class GameState {

    constructor(
        public turn: string,
        public started: boolean,
        public finished: boolean,
        public checkSide: string | null = null,
        public checkPosition: string | null = null
    ) { }
}

export class GameFormat {

    private _name: string;
    private _white_remainig: number;
    private _black_remainig: number;
    private _move_increment: number

    constructor(name: string, white_remainig: number, black_remainig: number, move_increment: number) {
        this._name = name;
        this._white_remainig = white_remainig;
        this._black_remainig = black_remainig;
        this._move_increment = move_increment;
    }

    get white_remainig() {
        return this._white_remainig;
    }

    get black_remainig() {
        return this._black_remainig;
    }

    get move_increment() {
        return this._move_increment;
    }
}