import { Board } from "src/app/pages/game/play/play/models/board/board";
import { Movement } from "src/app/services/models/movement";
import { Cell } from "../board/ cell";
import { Side } from "../side";
import { KingCastledEvent } from "../events/game-event";

export class ChessGame {

    private _id: string;
    private _name: string;
    private _format: GameFormat;
    private _board: Board;
    private _whiteTimer: number;
    private _blackTimer: number;
    private _turn: Side;
    private _checkSide: string | null = null;
    private _checkPosition: string | null = null;

    public history: Movement[];

    constructor(id: string, name: string, format: GameFormat, board: Board, turn: Side) {
        this._id = id;
        this._name = name;
        this._format = format;
        this._board = board;
        this.history = [];
        this._whiteTimer = format.remaining;
        this._blackTimer = format.remaining;
        this._turn = turn;
    }

    public setCheck(side: string | null, position: string | null) {
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
                const entry = new Movement(this.id, piece, from_.id, to.id, capturedPiece);
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
                    const entry = new Movement(this.id, piece, from_.id, to.id);
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
            this._board.movePiece(kingFrom, kingTo);
            this._board.movePiece(rookFrom, rookTo);

            // Record king's move on castling, rook's move is implicit in the move entry
            const piece = this._board.getPiece(kingTo);
            if (piece) {
                const entry = new Movement(this.id, piece, kingFrom.id, kingTo.id);
                this.history.push(entry);
            }

            this.switchTurn();
        }
    }

    public rollbackMove() {
        const lastMove = this.history.pop();
        if (lastMove) {
            this._board.revertMove(lastMove.from, lastMove.to, lastMove.capturedPiece);
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

    private switchTurn() {
        this._turn = (this._turn == Side.black) ? Side.white : Side.black;
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
    private _remaining: number;
    private _additional: number;

    constructor(name: string, remaining: number, additional: number) {
        this._name = name;
        this._remaining = remaining;
        this._additional = additional;
    }

    get remaining() {
        return this._remaining;
    }
}