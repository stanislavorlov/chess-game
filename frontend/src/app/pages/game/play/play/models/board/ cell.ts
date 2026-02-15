import { Piece } from "../pieces/piece";

export class Cell {

    private _file: string;
    private _rank: number;
    private _piece: Piece | null;
    private _color: string;
    private _selected: boolean = false;
    private _checked: boolean = false;
    private _isHeader: boolean;
    private _headerLabel: string;

    constructor(file: string, rank: number, color: string, piece: Piece | null, isHeader: boolean = false, headerLabel: string = '') {
        this._file = file;
        this._rank = rank;
        this._color = color;
        this._piece = piece;
        this._isHeader = isHeader;
        this._headerLabel = headerLabel;
    }

    get isHeader() {
        return this._isHeader;
    }

    get headerLabel() {
        return this._headerLabel;
    }

    get selected() {
        return this._selected;
    }

    set selected(value: boolean) {
        this._selected = value;
    }

    get checked() {
        return this._checked;
    }

    set checked(value: boolean) {
        this._checked = value;
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