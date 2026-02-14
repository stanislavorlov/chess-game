import { Piece } from "src/app/pages/game/play/play/models/pieces/piece";
import { PieceFactory } from "src/app/pages/game/play/play/models/pieces/piece_factory";
import { PieceType } from "src/app/pages/game/play/play/models/pieces/piece_type";
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
    private _flatBoard: Cell[] = [];
    private _cellsMap: Map<string, Cell> = new Map();
    private _files: string[] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
    private _ranks: number[] = [8, 7, 6, 5, 4, 3, 2, 1];

    constructor(squares: SquareDto[]) {
        // First, create a map of all squares for easy access
        squares.forEach((square: SquareDto) => {
            const [file, rank] = [square.square[0], square.rank];
            let piece: Piece | null = null;
            if (!!square.piece) {
                piece = PieceFactory.getPiece(square.piece);
            }
            const cell = new Cell(file, Number(rank), square.color, piece);
            this._cellsMap.set(cell.id, cell);
        });

        this.buildFlatBoard();
    }

    private buildFlatBoard() {
        this._flatBoard = [];

        // Top row: empty corner + file headers (a-h)
        this._flatBoard.push(new Cell('', 0, '', null, true, ''));
        this._files.forEach(f => {
            this._flatBoard.push(new Cell(f, 0, '', null, true, f));
        });

        // Rows 8 to 1: Rank header + cells
        this._ranks.forEach(rank => {
            this._flatBoard.push(new Cell('', rank, '', null, true, rank.toString()));
            this._files.forEach(file => {
                const squareId = `${file}${rank}`.toLowerCase();
                const cell = this._cellsMap.get(squareId);
                if (cell) {
                    this._flatBoard.push(cell);
                }
            });
        });
    }

    public initialize() {
        this._cellsMap.clear();

        const setup = [
            { rank: 1, pieces: [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook], side: Side.white },
            { rank: 2, pieces: Array(8).fill(Pawn), side: Side.white },
            { rank: 7, pieces: Array(8).fill(Pawn), side: Side.black },
            { rank: 8, pieces: [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook], side: Side.black }
        ];

        for (let rank = 1; rank <= 8; rank++) {
            for (let i = 0; i < 8; i++) {
                const file = this._files[i];
                const color = (rank + i) % 2 === 0 ? 'B' : 'W';
                const squareId = `${file}${rank}`.toLowerCase();

                let piece: Piece | null = null;
                const rowSetup = setup.find(s => s.rank === rank);
                if (rowSetup) {
                    const PieceClass = rowSetup.pieces[i];
                    piece = new PieceClass('', rowSetup.side);
                }

                const cell = new Cell(file, rank, color, piece);
                this._cellsMap.set(squareId, cell);
            }
        }
        this.buildFlatBoard();
    }

    get flatBoard() {
        return this._flatBoard;
    }

    public getCell(id: string): Cell | undefined {
        return this._cellsMap.get(id.toLowerCase());
    }

    isValidMove(from: Cell, to: Cell): boolean {
        let cell = this.getCell(from.id);
        let piece = cell?.piece;

        if (!!piece && piece.validateMove(from, to)) {
            if (piece.can_move_over) {
                return true;
            }

            if (piece.type == PieceType.Pawn) {
                let step = from.rank > to.rank ? -1 : 1;
                for (let i of this.range(from.rank + step, to.rank, step)) {
                    let intermediateCell = this.getCell(`${from.file}${i}`);
                    if (intermediateCell?.piece != null) {
                        return false;
                    }
                }
            } else if (piece.type == PieceType.Rook) {
                // ToDo: Implement rook path validation
            }
            // ... other piece validations
            return true;
        }

        return false;
    }

    range(start: number, stop: number, step: number = 1): number[] {
        const result = [];
        if (step > 0) {
            for (let i = start; i < stop; i += step) result.push(i);
        } else {
            for (let i = start; i > stop; i += step) result.push(i);
        }
        return result;
    }

    public revertMove(fromId: string, toId: string, capturedPiece?: Piece | null) {
        const fromCell = this.getCell(fromId);
        const toCell = this.getCell(toId);

        if (fromCell && toCell) {
            fromCell.piece = toCell.piece;
            toCell.piece = capturedPiece || null;
        }
    }
}