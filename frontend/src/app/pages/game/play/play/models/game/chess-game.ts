import { Board } from "src/app/pages/game/play/play/models/board/board";
import { Movement } from "src/app/services/models/movement";
import { Cell } from "../board/ cell";
import { Side } from "../side";

export class ChessGame {

    private _id: string;
    private _name: string;
    private _format: GameFormat;
    private _board: Board;
    private _whiteTimer: number;
    private _blackTimer: number;
    private _turn: Side;

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
        const isTurnFollowed = from_.piece?.side?.value == this._turn.value;
        const isValidMove = this._board.isValidMove(from_, to);
        if (isValidMove && isTurnFollowed) {
            const capturedPiece = to.piece;
            to.piece = from_.piece;
            from_.piece = null;

            if (!!to.piece) {
                const entry = new Movement(this.id, to.piece, from_.id, to.id, capturedPiece);
                this.history.push(entry);
            }

            this.switchTurn();
            return true;
        } else {
            console.log(`Invalid move. Valid move: ${isValidMove}, turn followed: ${isTurnFollowed}`);
        }

        return false;
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


    constructor(turn: string, started: boolean, finished: boolean) {

    }
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