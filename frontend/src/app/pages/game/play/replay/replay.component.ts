import { Component, inject, OnDestroy, OnInit, ChangeDetectionStrategy, ChangeDetectorRef, DestroyRef } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { NgClass, NgFor, NgIf, TitleCasePipe } from '@angular/common';
import { ChessService } from 'src/app/services/chess.service';
import { ChessGameDto } from 'src/app/services/models/chess-game-dto';
import { ActivatedRoute } from '@angular/router';
import { ChessGame, GameFormat } from '../play/models/game/chess-game';
import { Board } from 'src/app/pages/game/play/play/models/board/board';
import { Cell } from '../play/models/board/ cell';
import { Side } from '../play/models/side';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

@Component({
  selector: 'app-replay',
  standalone: true,
  imports: [
    MatCardModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    NgClass, NgFor, NgIf, TitleCasePipe
  ],
  templateUrl: './replay.component.html',
  styleUrl: './replay.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class ReplayComponent implements OnInit, OnDestroy {
  private readonly route = inject(ActivatedRoute);
  private readonly destroyRef = inject(DestroyRef);
  private readonly cdr = inject(ChangeDetectorRef);
  
  public game: ChessGame | null = null;
  public isFlipped = false;
  public isLoading = true;

  // Replay state
  public allMoves: string[] = []; // UCI moves
  public currentMoveIndex = -1;
  public gameName = '';

  constructor(
    private chessService: ChessService
  ) { }

  ngOnInit(): void {
    this.route.paramMap.pipe(takeUntilDestroyed(this.destroyRef)).subscribe(params => {
      const gameId = params.get('id');
      if (gameId) {
        this.initializeReplay(gameId);
      }
    });
  }

  ngOnDestroy(): void {}

  private initializeReplay(gameId: string): void {
    this.isLoading = true;
    this.cdr.markForCheck();

    this.chessService.getGame(gameId).pipe(takeUntilDestroyed(this.destroyRef)).subscribe({
      next: (data: ChessGameDto) => {
        // Initialize an empty board to the starting state
        const board = new Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR');
        
        this.game = new ChessGame(
          data.game_id,
          data.name,
          new GameFormat('Standard', 0, 0, 0),
          board,
          Side.white
        );
        this.gameName = data.name;

        if (data.history) {
          this.allMoves = data.history.split(',').filter(m => m.length >= 4);
        }

        this.isLoading = false;
        this.cdr.markForCheck();
      },
      error: (err) => {
        console.error('Failed to load game for replay', err);
        this.isLoading = false;
        this.cdr.markForCheck();
      }
    });
  }

  public nextMove(): void {
    if (!this.game || this.currentMoveIndex >= this.allMoves.length - 1) return;

    this.currentMoveIndex++;
    const uci = this.allMoves[this.currentMoveIndex];
    this.applyUciMove(uci);
    this.cdr.markForCheck();
  }

  public prevMove(): void {
    if (!this.game || this.currentMoveIndex < 0) return;

    this.game.rollbackMove();
    this.currentMoveIndex--;
    this.cdr.markForCheck();
  }

  private applyUciMove(uci: string): void {
    if (!this.game) return;
    const fromSq = uci.substring(0, 2);
    const toSq = uci.substring(2, 4);
    const fromCell = this.game.board.cells.find(c => c.id === fromSq);
    const toCell = this.game.board.cells.find(c => c.id === toSq);

    if (fromCell && toCell) {
      // Bypassing some strict checks by treating it as legal
      this.game.movePiece(fromCell, toCell);
    }
  }

  // Board helpers
  getPiece(cell: Cell) {
    return this.game?.board.getPiece(cell);
  }

  getGridRow(rank: number): number {
    return this.isFlipped ? rank : 9 - rank;
  }

  getGridColumn(file: string): number {
    const fileIndex = file.charCodeAt(0) - 'a'.charCodeAt(0) + 1;
    return this.isFlipped ? 9 - fileIndex : fileIndex;
  }

  shouldShowRankCoordinate(cell: Cell): boolean {
    if (cell.isHeader) return false;
    return this.isFlipped ? cell.file === 'h' : cell.file === 'a';
  }

  shouldShowFileCoordinate(cell: Cell): boolean {
    if (cell.isHeader) return false;
    return this.isFlipped ? cell.rank === 8 : cell.rank === 1;
  }

  getTopPlayer() {
    return this.isFlipped ? { label: 'White' } : { label: 'Black' };
  }

  getBottomPlayer() {
    return this.isFlipped ? { label: 'Black' } : { label: 'White' };
  }
}
