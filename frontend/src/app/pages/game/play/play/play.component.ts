import { Component, inject, NgZone, OnDestroy, OnInit, ChangeDetectionStrategy, ChangeDetectorRef, DestroyRef } from '@angular/core';
import { MatSelectModule } from '@angular/material/select';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatRadioModule } from '@angular/material/radio';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { NgClass, NgFor, NgIf, TitleCasePipe } from '@angular/common';
import { MoveFailureDialogComponent } from './move-failure-dialog/move-failure-dialog.component';
import { GameOverDialogComponent } from './game-over-dialog/game-over-dialog.component';
import { ChessService } from 'src/app/services/chess.service';
import { CreateGame } from './models/create-game';
import { ChessGameDto } from 'src/app/services/models/chess-game-dto';
import { ActivatedRoute, Router } from '@angular/router';
import { PlayService } from 'src/app/services/play.service';
import { ChessGame, GameFormat } from './models/game/chess-game';
import { Board } from 'src/app/pages/game/play/play/models/board/board';
import { Cell } from './models/board/ cell';
import { SanMovement } from 'src/app/services/models/movement';
import { Side } from './models/side';
import { TimeControlOption, TIME_OPTIONS_MAP } from './models/game-time-option';
import * as DomainEvents from './models/events/game-event';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

@Component({
  selector: 'app-play',
  imports: [
    MatFormFieldModule,
    MatSelectModule,
    FormsModule,
    ReactiveFormsModule,
    MatRadioModule,
    MatButtonModule,
    MatCardModule,
    MatInputModule,
    MatCheckboxModule,
    MatSnackBarModule,
    MatDialogModule,
    NgFor, NgIf, TitleCasePipe
  ],
  templateUrl: './play.component.html',
  styleUrl: './play.component.scss',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PlayComponent implements OnInit, OnDestroy {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly destroyRef = inject(DestroyRef);
  private readonly cdr = inject(ChangeDetectorRef);
  
  private selectedSquare: Cell | null = null;
  private gameTimer: any;
  private readonly playService = inject(PlayService);

  public formats: string[];
  public selectedFormat = '';
  public selectedTimeOption: TimeControlOption | null = null;
  public selectedMode = 'bot';
  public selectedSide = 'random';
  public game!: ChessGame;
  public isFlipped = false;

  get currentTurn(): string {
    return this.game?.turn?.value || 'W';
  }

  get currentTimeOptions(): TimeControlOption[] {
    return TIME_OPTIONS_MAP[this.selectedFormat] || [];
  }

  constructor(
    private chessService: ChessService,
    private snackBar: MatSnackBar,
    private dialog: MatDialog
  ) {
    this.formats = Object.keys(TIME_OPTIONS_MAP);

    this.selectedFormat = this.formats[1];
  }

  formatSeconds(totalSeconds: number): string {
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = Math.floor(totalSeconds % 60);

    return minutes.toString() + 'm ' + seconds.toString().padStart(2, '0') + 's';
  }

  gameInitialized(): boolean {
    return !!this.game && this.game.id !== '';
  }

  private zone = inject(NgZone);

  ngOnInit(): void {
    this.route.paramMap.pipe(takeUntilDestroyed(this.destroyRef)).subscribe(params => {
      const gameId = params.get('id');
      this.initializeGame(gameId);
      this.cdr.markForCheck();
    });
  }

  private initializeGame(gameId: string | null): void {
    if (this.gameTimer) {
      clearInterval(this.gameTimer);
    }

    if (!!gameId) {
      this.playService.setGameId(gameId);
      this.chessService.getGame(gameId).pipe(takeUntilDestroyed(this.destroyRef)).subscribe((data: ChessGameDto) => {
        this.game = new ChessGame(
          data.game_id,
          data.name,
          new GameFormat(
            data.game_format.value,
            data.game_format.white_remaining_time,
            data.game_format.black_remaining_time,
            data.game_format.move_increment),
          new Board(data.board),
          Side.parse(data.state.turn));

        this.game.syncState(Side.parse(data.state.turn), data.state.legal_moves);
        if (!!data.state.check_side && !!data.state.check_position) {
          this.game.setCheck(Side.parse(data.state.check_side), data.state.check_position);
        }

        let that = this;

        if (data.history) {
          data.history.split(',').forEach((san: string) => {
            const historyMove = new SanMovement(that.game.id, san);
            that.game.history.push(historyMove);
          });
        }

        if (data.state.finished) {
          this.dialog.open(GameOverDialogComponent, {
            data: {
              result: that.game.checkSide == Side.black ? 'White wins' : 'Black wins',
              finished_date: ''
            },
            width: '350px'
          });
        }

        this.gameTimer = setInterval(function () {
          if (that.game) {
            that.game.timerTick();
            that.cdr.markForCheck();
          }
        }, 1000);
        this.cdr.markForCheck();
      });

      this.playService.getMessages().pipe(takeUntilDestroyed(this.destroyRef)).subscribe((data: unknown) => {
        this.zone.run(() => {
          try {
            console.log('received message:', data);
            const event = DomainEvents.GameEventFactory.fromRaw(data);
            if (!event || event.game_id !== this.game.id) {
              console.log('Skipping event (wrong game or null):', event?.game_id);
              return;
            }

            console.log('Processing event:', event.event_type);

            if (event instanceof DomainEvents.PieceMoveFailedEvent) {
              console.warn('Move failed on server:', event.reason);
              this.game.rollbackMove();

              this.dialog.open(MoveFailureDialogComponent, {
                data: {
                  reason: event.reason || 'Illegal move',
                  from_: event.from_,
                  to: event.to
                },
                width: '350px'
              });
            } else if (event instanceof DomainEvents.KingCastledEvent) {
              this.game.castleKing(event);
            } else if (event instanceof DomainEvents.PieceMovedEvent || event instanceof DomainEvents.PieceCapturedEvent) {
              // Reset check state on any move; if a new check occurs, a king-checked event will follow
              console.log('Piece moved/captured event, clearing check');
              this.game.clearCheck();
            } else if (event instanceof DomainEvents.KingCheckedEvent || event instanceof DomainEvents.KingCheckmatedEvent) {
              console.log('King check state update:', event.event_type, event.side);
              this.game.setCheck(Side.parse(event.side), event.position);
            } else if (event instanceof DomainEvents.SyncedStateEvent) {
              console.log('SyncedState received, turn:', event.turn.name);
              this.game.syncState(event.turn, event.legal_moves);
            } else if (event instanceof DomainEvents.AiPredictedMoveEvent) {
              console.log('AI predicted move:', event.predicted_ai_move);
              const uci = event.predicted_ai_move;
              if (uci && uci.length >= 4) {
                const fromSq = uci.substring(0, 2);
                const toSq = uci.substring(2, 4);
                const fromCell = this.game.board.cells.find(c => c.id === fromSq);
                const toCell = this.game.board.cells.find(c => c.id === toSq);
                if (fromCell && toCell) {
                  if (this.game.movePiece(fromCell, toCell)) {
                    let historyEntry = this.game.history.at(-1);
                    this.playService.sendMessage(historyEntry);
                  }
                }
              }
            } else if (event instanceof DomainEvents.GameFinishedEvent) {
              console.log('Game finished:', event.result);
              this.dialog.open(GameOverDialogComponent, {
                data: {
                  result: event.result,
                  finished_date: event.finished_date
                },
                width: '350px'
              });
            }
            this.cdr.markForCheck();
          } catch (e) {
            console.error('Error parsing WebSocket message', e);
          }
        });
      });
    } else {
      this.game = this.chessService.newGame();
      this.cdr.markForCheck();
    }
  }

  ngOnDestroy(): void {
    if (!!this.gameTimer) {
      clearInterval(this.gameTimer);
    }
  }

  startGame(): void {
    const new_game = new CreateGame();
    new_game.increment = parseInt(this.selectedTimeOption?.incrementPerMove || '0', 10);
    new_game.format = this.selectedFormat;
    new_game.baseTime = parseInt(this.selectedTimeOption?.baseTime || '0', 10);

    if (this.selectedMode === 'bot') {
      new_game.color = this.selectedSide;
      new_game.difficulty = "1";

      this.chessService.startGame(new_game).pipe(takeUntilDestroyed(this.destroyRef)).subscribe((data: ChessGameDto) => {
        let gameId = data.game_id;
        this.router.navigate(['/play', gameId]);
      });
    } else {
      this.chessService.startOnlineGame(new_game).pipe(takeUntilDestroyed(this.destroyRef)).subscribe((data: unknown) => {
        this.snackBar.open("Searching for opponent...", "Close", { duration: 3000 });
      });
    }
  }

  selectTime(option: TimeControlOption): void {
    this.selectedTimeOption = option;
    this.cdr.markForCheck();
  }

  getPiece(cell: Cell) {
    return this.game.board.getPiece(cell);
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

  clickBoard(square: Cell): void {
    if (!this.gameInitialized()) return;

    if (!!this.selectedSquare) {
      this.selectedSquare.selected = false;

      if (!!this.getPiece(this.selectedSquare)) {
        if (this.game.movePiece(this.selectedSquare, square)) {
          let historyEntry = this.game.history.at(-1);

          this.playService.sendMessage(historyEntry);
        }
      }

      this.selectedSquare = null;

    } else {
      const piece = this.getPiece(square);
      if (!piece) return;

      if (!this.game.isSelectable(square)) return;

      square.selected = true;
      this.selectedSquare = square;
    }
    this.cdr.markForCheck();
  }

  updateBoardCheckState(): void {
    if (!this.game) return;

    this.game.board.cells.forEach(cell => {
      cell.checked = !cell.isHeader && !!this.game.checkPosition && cell.id === this.game.checkPosition.toLowerCase();
    });
    this.cdr.markForCheck();
  }

  getTopPlayer() {
    return this.isFlipped ? { side: Side.white, label: 'Player 1 (White)' } : { side: Side.black, label: 'Player 2 (Black)' };
  }

  getBottomPlayer() {
    return this.isFlipped ? { side: Side.black, label: 'Player 2 (Black)' } : { side: Side.white, label: 'Player 1 (White)' };
  }
}