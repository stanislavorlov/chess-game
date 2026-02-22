import { Board } from './board';
import { Cell } from './ cell';
import { Side } from '../side';
import { PieceType } from '../pieces/piece_type';
import { PieceFactory } from '../pieces/piece_factory';
import { SquareDto } from 'src/app/services/models/chess-game-dto';

describe('Board', () => {
    let board: Board;

    // Helper to create a starting board DTO
    const createStartingBoardDto = (): SquareDto[] => {
        const squares: SquareDto[] = [];
        const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
        const ranks = [1, 2, 3, 4, 5, 6, 7, 8];

        for (const rank of ranks) {
            for (const file of files) {
                let piece = null;
                if (rank === 2) piece = { abbreviation: 'wp', moved: false };
                if (rank === 7) piece = { abbreviation: 'bp', moved: false };
                if (rank === 1) {
                    if (file === 'a' || file === 'h') piece = { abbreviation: 'wr', moved: false };
                    if (file === 'b' || file === 'g') piece = { abbreviation: 'wn', moved: false };
                    if (file === 'c' || file === 'f') piece = { abbreviation: 'wb', moved: false };
                    if (file === 'd') piece = { abbreviation: 'wq', moved: false };
                    if (file === 'e') piece = { abbreviation: 'wk', moved: false };
                }
                if (rank === 8) {
                    if (file === 'a' || file === 'h') piece = { abbreviation: 'br', moved: false };
                    if (file === 'b' || file === 'g') piece = { abbreviation: 'bn', moved: false };
                    if (file === 'c' || file === 'f') piece = { abbreviation: 'bb', moved: false };
                    if (file === 'd') piece = { abbreviation: 'bq', moved: false };
                    if (file === 'e') piece = { abbreviation: 'bk', moved: false };
                }

                squares.push({
                    square: `${file}${rank}`,
                    rank: rank,
                    color: (rank + files.indexOf(file)) % 2 === 0 ? 'B' : 'W',
                    piece: piece
                });
            }
        }
        return squares;
    };

    beforeEach(() => {
        const squares = createStartingBoardDto();
        board = new Board(squares);
    });

    it('should initialize with correct piece positions', () => {
        const e2 = board.getCell('e2')!;
        const e7 = board.getCell('e7')!;
        const e1 = board.getCell('e1')!;

        expect(board.getPiece(e2)?.type).toBe(PieceType.Pawn);
        expect(board.getPiece(e2)?.side).toBe(Side.white);

        expect(board.getPiece(e7)?.type).toBe(PieceType.Pawn);
        expect(board.getPiece(e7)?.side).toBe(Side.black);

        expect(board.getPiece(e1)?.type).toBe(PieceType.King);
        expect(board.getPiece(e1)?.side).toBe(Side.white);
    });

    it('should validate pawn opening move (push 2 squares)', () => {
        const e2 = board.getCell('e2')!;
        const e4 = board.getCell('e4')!;
        const e3 = board.getCell('e3')!;

        expect(board.isValidMove(e2, e4)).toBeTrue();
        expect(board.isValidMove(e2, e3)).toBeTrue();
    });

    it('should validate knight moves', () => {
        const g1 = board.getCell('g1')!;
        const f3 = board.getCell('f3')!;
        const h3 = board.getCell('h3')!;
        const e2 = board.getCell('e2')!;

        expect(board.isValidMove(g1, f3)).toBeTrue();
        expect(board.isValidMove(g1, h3)).toBeTrue();
        expect(board.isValidMove(g1, e2)).toBeFalse(); // Occupied by own piece
    });

    it('should detect captures correctly', () => {
        // Manually place a black pawn on e3 to test capture by white pawn on d2
        const d2 = board.getCell('d2')!;
        const e3 = board.getCell('e3')!;

        // Simulate black pawn on e3
        const blackPawn = PieceFactory.getPiece({ abbreviation: 'bp', moved: false });
        (board as any)._pieceMap.set(e3, blackPawn);

        expect(board.isValidMove(d2, e3)).toBeTrue();
    });

    it('should detect check', () => {
        // Place a black rook on e8 and white king on e1, clear path
        const e1 = board.getCell('e1')!;
        const e8 = board.getCell('e8')!;

        // Clear e2-e7
        for (let i = 2; i <= 7; i++) {
            const cell = board.getCell(`e${i}`)!;
            (board as any)._pieceMap.set(cell, null);
        }

        // Ensure e8 has a black rook
        const blackRook = PieceFactory.getPiece({ abbreviation: 'br', moved: false });
        (board as any)._pieceMap.set(e8, blackRook);

        expect(board.isCheck(Side.white)).toBeTrue();
    });

    it('should identify basic castling move', () => {
        const e1 = board.getCell('e1')!;
        const g1 = board.getCell('g1')!;

        // Clear path for kingside castling
        const f1 = board.getCell('f1')!;
        const g1_cell = board.getCell('g1')!;
        (board as any)._pieceMap.set(f1, null);
        (board as any)._pieceMap.set(g1_cell, null);

        expect(board.isCastlingMove(e1, g1)).toBeTrue();
    });
});
