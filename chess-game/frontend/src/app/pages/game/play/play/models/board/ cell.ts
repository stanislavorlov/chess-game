import { Piece } from "../pieces/piece";

export class Cell {

    private _file: string;
    private _rank: number;
    private _piece: Piece | null;
    private _color: string;

    constructor(file: string, rank: number, color: string, piece: Piece | null) {
        this._file = file;
        this._rank = rank;
        this._color = color;
        this._piece = piece;
    }

    get file() {
        return this._file;
    }

    get rank() {
        return this._rank;
    }

    get color() {
        return this._color;
    }

    get piece() {
        return this._piece;
    }

    set piece(value: Piece | null) {
        this._piece = value;
    }

    get id() {
        return `${this._file}${this._rank}`.toLowerCase();
    }
}