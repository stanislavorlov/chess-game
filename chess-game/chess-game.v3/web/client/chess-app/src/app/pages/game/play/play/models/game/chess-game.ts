import { Board } from "src/app/pages/game/play/play/models/board/board";
import { Movement } from "src/app/services/models/movement";

export class ChessGame {

    private _id: string;
    private _name: string;
    private _format: GameFormat;
    private _board: Board;

    constructor(id: string, name: string, format: GameFormat, board: Board) {
        this._id = id;
        this._name = name;
        this._format = format;
        this._board = board;
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