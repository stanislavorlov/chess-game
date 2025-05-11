import { Piece } from "src/app/pages/game/play/play/models/pieces/piece";
import { PieceFactory } from "src/app/pages/game/play/play/models/pieces/piece_factory";
import { PieceType } from "src/app/pages/game/play/play/models/pieces/piece_type";
import { Direction } from "../../../../../../services/models/direction";
import { Cell } from "./ cell";
import { SquareDto } from "src/app/services/models/chess-game-dto";
import { Rook } from "../pieces/rook";
import { Side } from "../side";
import { Pawn } from "../pieces/pawn";
import { Knight } from "../pieces/knight";
import { Bishop } from "../pieces/bishop";
import { Queen } from "../pieces/queen";
import { King } from "../pieces/king";

export class Board {
    private _board: Record<number, Cell[]>;
    private _files: string[] = ['a','b','c','d','e','f','g','h'];
    private _ranks: number[] = [1,2,3,4,5,6,7,8];

    constructor(squares: SquareDto[]) {
        this._board = {};

        let that = this;

        squares.forEach(function (square: SquareDto) {
            const [file,rank] = [square.square[0], square.rank];
            
            if (!that._board[rank]) {
                that._board[rank] = [];
            }

            let piece: Piece | null = null;
            if (!!square.piece) {
                piece = PieceFactory.getPiece(square.piece);
            }
            that._board[rank].push(new Cell(file, Number(rank), square.color, piece));
        });
    }

    public initialize() {
        // chess board for new game
        this._board[1] = [
            new Cell('a', 1, 'B', new Rook('', Side.white)),
            new Cell('b', 1, 'W', new Knight('', Side.white)),
            new Cell('c', 1, 'B', new Bishop('', Side.white)),
            new Cell('d', 1, 'W', new Queen('', Side.white)),
            new Cell('e', 1, 'B', new King('', Side.white)),
            new Cell('f', 1, 'W', new Bishop('', Side.white)),
            new Cell('g', 1, 'B', new Knight('', Side.white)),
            new Cell('h', 1, 'W', new Rook('', Side.white)),
        ];
        this._board[2] = [
            new Cell('a', 2, 'W', new Pawn('', Side.white)),
            new Cell('b', 2, 'B', new Pawn('', Side.white)),
            new Cell('c', 2, 'W', new Pawn('', Side.white)),
            new Cell('d', 2, 'B', new Pawn('', Side.white)),
            new Cell('e', 2, 'W', new Pawn('', Side.white)),
            new Cell('f', 2, 'B', new Pawn('', Side.white)),
            new Cell('g', 2, 'W', new Pawn('', Side.white)),
            new Cell('h', 2, 'B', new Pawn('', Side.white)),
        ];
        this._board[3] = [
            new Cell('a', 3, 'B', null),
            new Cell('b', 3, 'W', null),
            new Cell('c', 3, 'B', null),
            new Cell('d', 3, 'W', null),
            new Cell('e', 3, 'B', null),
            new Cell('f', 3, 'W', null),
            new Cell('g', 3, 'B', null),
            new Cell('h', 3, 'W', null),
        ];
        this._board[4] = [
            new Cell('a', 4, 'W', null),
            new Cell('b', 4, 'B', null),
            new Cell('c', 4, 'W', null),
            new Cell('d', 4, 'B', null),
            new Cell('e', 4, 'W', null),
            new Cell('f', 4, 'B', null),
            new Cell('g', 4, 'W', null),
            new Cell('h', 4, 'B', null),
        ];
        this._board[5] = [
            new Cell('a', 5, 'B', null),
            new Cell('b', 5, 'W', null),
            new Cell('c', 5, 'B', null),
            new Cell('d', 5, 'W', null),
            new Cell('e', 5, 'B', null),
            new Cell('f', 5, 'W', null),
            new Cell('g', 5, 'B', null),
            new Cell('h', 5, 'W', null),
        ];
        this._board[6] = [
            new Cell('a', 6, 'W', null),
            new Cell('b', 6, 'B', null),
            new Cell('c', 6, 'W', null),
            new Cell('d', 6, 'B', null),
            new Cell('e', 6, 'W', null),
            new Cell('f', 6, 'B', null),
            new Cell('g', 6, 'W', null),
            new Cell('h', 6, 'B', null),
        ];
        this._board[7] = [
            new Cell('a', 7, 'B', new Pawn('', Side.black)),
            new Cell('b', 7, 'W', new Pawn('', Side.black)),
            new Cell('c', 7, 'B', new Pawn('', Side.black)),
            new Cell('d', 7, 'W', new Pawn('', Side.black)),
            new Cell('e', 7, 'B', new Pawn('', Side.black)),
            new Cell('f', 7, 'W', new Pawn('', Side.black)),
            new Cell('g', 7, 'B', new Pawn('', Side.black)),
            new Cell('h', 7, 'W', new Pawn('', Side.black)),
        ];
        this._board[8] = [
            new Cell('a', 8, 'W', new Rook('', Side.black)),
            new Cell('b', 8, 'B', new Knight('', Side.black)),
            new Cell('c', 8, 'W', new Bishop('', Side.black)),
            new Cell('d', 8, 'B', new Queen('', Side.black)),
            new Cell('e', 8, 'W', new King('', Side.black)),
            new Cell('f', 8, 'B', new Bishop('', Side.black)),
            new Cell('g', 8, 'W', new Knight('', Side.black)),
            new Cell('h', 8, 'B', new Rook('', Side.black)),
        ];
    }

    get ranks() {
        return this._ranks;
    }

    public files(rank: number) {
        return this._board[rank];
    }

    private groupBy = <T, K extends keyof any>(arr: T[], key: (i: T) => K) =>
        arr.reduce((groups, item) => {
          (groups[key(item)] ||= []).push(item);
          return groups;
        }, {} as Record<K, T[]>);

    isValidMove(from: Cell, to: Cell) : boolean {
        const [file,rank] = [from.file, from.rank];
        const direction = from.rank > to.rank ? Direction.Up : Direction.Down;

        let piece = this._board[from.rank].find(f => f.file == from.file)?.piece;
        if (!!piece && piece.validateMove(from, to)) {
            // Knight
            if (piece.can_move_over) {
                return true;
            }

            const [toFile,toRank] = [to.file,to.rank];

            if (piece.type == PieceType.Pawn) {
                let step = rank > toRank ? -1 : 1;
                for (let i of this.range(rank + step, toRank, step)) {
                    let cell = this._board[i].find(f => f.file == file);
                    if (cell?.piece != null) {
                        return false;
                    }
                }

            } else if (piece.type == PieceType.Rook) {
                // ToDo: Up, Down, Left, Right
                
            } else if (piece.type == PieceType.Bishop) {

            } else if (piece.type == PieceType.Queen) {

            } else if (piece.type == PieceType.King) {

            }

            return true;
        }

        return false;
    }

    //ToDo: move to utils
    range(start: number, stop: number, step: number = 1): number[] {
        const result = [];
        for (let i = start; i < stop; i+= step) {
            result.push(i);
        }

        return result;
    }
}