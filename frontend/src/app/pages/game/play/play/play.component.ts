import { Component, inject, OnDestroy, OnInit } from '@angular/core';
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
import { NgFor, NgIf, TitleCasePipe } from '@angular/common';
import { MoveFailureDialogComponent } from './move-failure-dialog/move-failure-dialog.component';
import { ChessService } from 'src/app/services/chess.service';
import { CreateGame } from './models/create-game';
import { ChessGameDto, HistoryEntryDto } from 'src/app/services/models/chess-game-dto';
import { ActivatedRoute, Router } from '@angular/router';
import { PlayService } from 'src/app/services/play.service';
import { ChessGame, GameFormat } from './models/game/chess-game';
import { Board } from 'src/app/pages/game/play/play/models/board/board';
import { Cell } from './models/board/ cell';
import { Movement } from 'src/app/services/models/movement';
import { PieceFactory } from './models/pieces/piece_factory';
import { Side } from './models/side';
import { TimeControlOption, TIME_OPTIONS_MAP } from './models/game-time-option';
import * as DomainEvents from './models/events/game-event';

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
  styleUrl: './play.component.scss'
})
export class PlayComponent implements OnInit, OnDestroy {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private selectedSquare: Cell | null = null;
  private gameTimer: NodeJS.Timeout;
  private playService: PlayService;

  public formats: string[];
  public selectedFormat = '';
  public selectedTimeOption: TimeControlOption | null = null;
  public game: ChessGame;
  public isFlipped = false;

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
    const seconds = totalSeconds % 60;

    return minutes.toString() + 'm ' + seconds.toString().padStart(2, '0') + 's';
  }

  gameInitialized(): boolean {
    const gameId = this.route.snapshot.paramMap.get('id');

    return gameId != null;
  }

  ngOnInit(): void {
    const gameId = this.route.snapshot.paramMap.get('id');

    if (!!gameId) {
      this.playService = new PlayService(gameId);
      this.chessService.getGame(gameId).subscribe((data: ChessGameDto) => {
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
        this.game.setCheck(data.state.check_side, data.state.check_position);

        let that = this;

        data.history.forEach(function (value: HistoryEntryDto) {
          let piece = PieceFactory.getPiece(value.piece);

          that.game.history.push(Movement.create(that.game.id, piece, value.from, value.to).withSan(value.san));
        });

        this.gameTimer = setInterval(function () {
          that.game.timerTick();
        }, 1000);
      });

      this.playService.getMessages().subscribe(data => {
        try {
          console.log('received message:', data);
          const event = DomainEvents.GameEventFactory.fromRaw(data);
          if (!event) return;

          if (event instanceof DomainEvents.PieceMoveFailedEvent && event.game_id === this.game.id) {
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
            this.game.clearCheck();
          } else if (event instanceof DomainEvents.KingCheckedEvent || event instanceof DomainEvents.KingCheckmatedEvent) {
            this.game.setCheck(event.side, event.position);

            // ToDo: handle checkmate (disable board, show message, etc.)
          } else if (event instanceof DomainEvents.SyncedStateEvent) {
            this.game.syncState(event.turn, event.legal_moves);
          }
        } catch (e) {
          console.error('Error parsing WebSocket message', e);
        }
      });
    } else {
      this.game = this.chessService.newGame();
    }
  }

  ngOnDestroy(): void {
    if (!!this.gameTimer) {
      clearInterval(this.gameTimer);
    }
  }

  startGame(): void {
    const new_game = new CreateGame();
    new_game.increment = this.selectedTimeOption?.incrementPerMove || '';
    new_game.format = this.selectedFormat;
    new_game.name = this.game.name;
    new_game.time = this.selectedTimeOption?.baseTime || '';

    this.chessService.startGame(new_game).subscribe((data: ChessGameDto) => {
      let gameId = data.game_id;

      this.router.navigate(['/play', gameId])
    });
  }

  selectTime(option: TimeControlOption): void {
    this.selectedTimeOption = option;
  }

  getPiece(cell: Cell) {
    return this.game.board.getPiece(cell);
  }

  getGridRow(rank: number): number {
    // 1-8 rank -> 2-9 row (grid is 1-indexed, row 1 is for file headers)
    return 10 - rank;
  }

  getGridColumn(file: string): number {
    // a-h -> 2-9 column
    return file.charCodeAt(0) - 'a'.charCodeAt(0) + 2;
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
  }

  updateBoardCheckState(): void {
    if (!this.game) return;

    this.game.board.cells.forEach(cell => {
      cell.checked = !cell.isHeader && !!this.game.checkPosition && cell.id === this.game.checkPosition.toLowerCase();
    });
  }

  getTopPlayer() {
    return this.isFlipped ? { side: Side.white, label: 'Player 1 (White)' } : { side: Side.black, label: 'Player 2 (Black)' };
  }

  getBottomPlayer() {
    return this.isFlipped ? { side: Side.black, label: 'Player 2 (Black)' } : { side: Side.white, label: 'Player 1 (White)' };
  }
}