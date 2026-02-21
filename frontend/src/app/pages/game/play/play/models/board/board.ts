import { Piece } from "src/app/pages/game/play/play/models/pieces/piece";
import { PieceFactory } from "src/app/pages/game/play/play/models/pieces/piece_factory";
import { Cell } from "./ cell";
import { SquareDto } from "src/app/services/models/chess-game-dto";
import { Rook } from "../pieces/rook";
import { Side } from "../side";
import { Pawn } from "../pieces/pawn";
import { Knight } from "../pieces/knight";
import { Bishop } from "../pieces/bishop";
import { Queen } from "../pieces/queen";
import { King } from "../pieces/king";
import { PieceType } from "../pieces/piece_type";

export class Board {
    private _files: string[] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
    private _ranks: number[] = [8, 7, 6, 5, 4, 3, 2, 1];
    private _pieceMap: Map<Cell, Piece | null> = new Map();

    constructor(squares: SquareDto[]) {
        // First, create a map of all squares for easy access
        squares.forEach((square: SquareDto) => {
            const [file, rank] = [square.square[0], square.rank];
            let piece: Piece | null = null;
            if (!!square.piece) {
                piece = PieceFactory.getPiece(square.piece);
                if (square.piece.moved) {
                    piece.markMoved();
                }
            }
            const cell = new Cell(file, Number(rank), square.color, false, '');
            this._pieceMap.set(cell, piece);
        });
    }

    public initialize() {
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

                let piece: Piece | null = null;
                const rowSetup = setup.find(s => s.rank === rank);
                if (rowSetup) {
                    const PieceClass = rowSetup.pieces[i];
                    piece = new PieceClass(rowSetup.side);
                }

                const cell = new Cell(file, rank, color, false, '');
                this._pieceMap.set(cell, piece);
            }
        }
    }

    get cells() {
        return Array.from(this._pieceMap.keys());
    }

    get files() {
        return this._files;
    }

    get ranks() {
        return this._ranks;
    }

    public getPiece(cell: Cell): Piece | null {
        return this._pieceMap.get(cell) || null;
    }

    public movePiece(from: Cell, to: Cell) {
        const piece = this._pieceMap.get(from);
        if (piece) {
            this._pieceMap.set(to, piece);
            this._pieceMap.set(from, null);
            piece.markMoved();
        }
    }

    public getCell(id: string): Cell | undefined {
        for (let cell of this._pieceMap.keys()) {
            if (cell.id === id.toLowerCase()) {
                return cell;
            }
        }
        return undefined;
    }

    public isUnderAttack(targetCell: Cell, attackerSide: Side): boolean {
        for (const [cell, piece] of this._pieceMap.entries()) {
            if (piece && piece.side.value === attackerSide.value) {
                if (this.isValidMove(cell, targetCell)) {
                    return true;
                }
            }
        }
        return false;
    }

    public isCheck(side: Side): boolean {
        const kingCell = this.findKing(side);
        if (!kingCell) return false;

        const opponentSide = side.value === Side.white.value ? Side.black : Side.white;
        return this.isUnderAttack(kingCell, opponentSide);
    }

    private findKing(side: Side): Cell | null {
        for (const [cell, piece] of this._pieceMap.entries()) {
            if (piece && piece.type === PieceType.King && piece.side.value === side.value) {
                return cell;
            }
        }
        return null;
    }

    public getLegalMoves(from: Cell): Cell[] {
        const piece = this.getPiece(from);
        if (!piece) return [];

        const legalMoves: Cell[] = [];
        const side = piece.side;

        // Iterate over all possible destination cells
        for (const to of this._pieceMap.keys()) {
            if (from === to) continue;

            // 1. Basic geometric and path validity
            const isBasicValid = this.isValidMove(from, to) || this.isCastlingMove(from, to);
            if (!isBasicValid) continue;

            // 2. Simulation: Make move and check if King is safe
            const targetPiece = this.getPiece(to);
            const originalPieceMoved = piece.moved;

            this.movePiece(from, to);
            const kingSafe = !this.isCheck(side);
            this.revertMove(from.id, to.id, targetPiece);

            // Restore moved state
            if (!originalPieceMoved) {
                piece.resetMoved();
            }

            if (kingSafe) {
                legalMoves.push(to);
            }
        }

        return legalMoves;
    }

    isValidMove(from: Cell, to: Cell): boolean {
        const piece = this._pieceMap.get(from);
        if (!piece) return false;

        const targetPiece = this._pieceMap.get(to);
        let isGeometricValid = false;

        if (targetPiece === null || targetPiece === undefined) {
            // "Push" move
            isGeometricValid = piece.validatePush(from, to);
        } else {
            // "Capture" move
            // Cannot capture own piece
            if (targetPiece.side.value === piece.side.value) return false;
            isGeometricValid = piece.validateCapture(from, to);
        }

        if (!isGeometricValid) return false;

        // Path check only for non-knights
        if (!piece.can_move_over) {
            if (!this.isPathClear(from, to)) {
                return false;
            }
        }

        return true;
    }

    isCastlingMove(from: Cell, to: Cell): boolean {
        const king = this._pieceMap.get(from);

        // 1. Guard: Must be a King that hasn't moved
        if (!king || king.type !== PieceType.King || king.moved) {
            return false;
        }

        // 2. Guard: Must be a strictly horizontal move
        if (from.rank !== to.rank) {
            return false;
        }

        // 3. Guard: Must be exactly a 2-square move
        const fileDiff = to.file.charCodeAt(0) - from.file.charCodeAt(0);
        if (Math.abs(fileDiff) !== 2) {
            return false;
        }

        // 4. Identify the expected Rook
        const isKingside = fileDiff > 0;
        const rookFile = isKingside ? 'h' : 'a';
        const rookCell = this.getCell(`${rookFile}${from.rank}`);

        // Guard: Cell must exist
        if (!rookCell) return false;

        const rook = this._pieceMap.get(rookCell);

        // 5. Guard: Must be a Rook that hasn't moved
        if (!rook || rook.type !== PieceType.Rook || rook.moved) {
            return false;
        }

        // 6. Check if the path is clear
        const step = isKingside ? 1 : -1;
        const startFileCode = from.file.charCodeAt(0);
        const endFileCode = rookCell.file.charCodeAt(0);

        for (let i = startFileCode + step; i !== endFileCode; i += step) {
            const intermediateCellId = `${String.fromCharCode(i)}${from.rank}`;
            const intermediateCell = this.getCell(intermediateCellId);

            // Guard: If there is a piece in the way, fail immediately
            if (intermediateCell && this._pieceMap.get(intermediateCell)) {
                return false;
            }
        }

        // missing three critical moves:
        // 7. Guard: King cannot be in check
        // 8. Guard: King cannot pass through a square that is under attack
        // 9. Guard: King cannot end up in check

        return true;
    }

    private isPathClear(from: Cell, to: Cell): boolean {
        const fileDiff = to.file.charCodeAt(0) - from.file.charCodeAt(0);
        const rankDiff = to.rank - from.rank;

        if (fileDiff === 0 && rankDiff === 0) return true;

        const fileStep = fileDiff === 0 ? 0 : (fileDiff > 0 ? 1 : -1);
        const rankStep = rankDiff === 0 ? 0 : (rankDiff > 0 ? 1 : -1);

        let currentFile = from.file.charCodeAt(0) + fileStep;
        let currentRank = from.rank + rankStep;

        const targetFile = to.file.charCodeAt(0);
        const targetRank = to.rank;

        while (currentFile !== targetFile || currentRank !== targetRank) {
            const squareId = `${String.fromCharCode(currentFile)}${currentRank}`.toLowerCase();
            const intermediateCell = this.getCell(squareId);
            if (!!intermediateCell && this._pieceMap.get(intermediateCell) !== null && this._pieceMap.get(intermediateCell) !== undefined) {
                return false;
            }
            currentFile += fileStep;
            currentRank += rankStep;
        }

        return true;
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
            this._pieceMap.set(fromCell, this._pieceMap.get(toCell) || null);
            this._pieceMap.set(toCell, capturedPiece || null);
        }
    }
}