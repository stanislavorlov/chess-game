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
import { NgFor, NgIf } from '@angular/common';
import { MoveFailureDialogComponent } from './move-failure-dialog/move-failure-dialog.component';
import { ChessService } from 'src/app/services/chess.service';
import { CreateGame } from './models/create-game';
import { ChessGameDto, HistoryEntryDto } from 'src/app/services/models/chess-game-dto';
import { ApiResult } from 'src/app/services/models/api-result';
import { ActivatedRoute, Router } from '@angular/router';
import { PlayService } from 'src/app/services/play.service';
import { ChessGame, GameFormat } from './models/game/chess-game';
import { Board } from 'src/app/pages/game/play/play/models/board/board';
import { TimeSelector } from './models/timeSelector';
import { Cell } from './models/board/ cell';
import { Movement } from 'src/app/services/models/movement';
import { PieceFactory } from './models/pieces/piece_factory';
import { Side } from './models/side';
import { GameTimeOption } from './models/game-time-option';
import { GameEventFactory, PieceMoveFailedEvent, PieceMovedEvent, PieceCapturedEvent, KingCheckedEvent, KingCheckmatedEvent } from './models/events/game-event';

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
    NgFor, NgIf
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

  public formats: TimeSelector[];
  public selectedFormat = '';
  public selectedTimeOption: GameTimeOption | null = null;
  public game: ChessGame;

  public timeOptionsMap: { [key: string]: GameTimeOption[] } = {
    'bullet': [
      { type: '1min', label: '1 mins', time: '0h1m', additional: '' },
      { type: '1|1min', label: '1|1 mins', time: '0h1m', additional: '0h1m' },
      { type: '2|1min', label: '2|1 mins', time: '0h2m', additional: '0h1m' }
    ],
    'blitz': [
      { type: '3min', label: '3 mins', time: '0h3m', additional: '' },
      { type: '3|2min', label: '3|2 mins', time: '0h3m', additional: '0h2m' },
      { type: '5min', label: '5 mins', time: '0h5m', additional: '' }
    ],
    'rapid': [
      { type: '10min', label: '10 mins', time: '0h10m', additional: '' },
      { type: '15|10min', label: '15|10 mins', time: '0h15m', additional: '0h10m' },
      { type: '30min', label: '30 mins', time: '0h30m', additional: '' }
    ]
  };

  get currentTimeOptions(): GameTimeOption[] {
    return this.timeOptionsMap[this.selectedFormat] || [];
  }

  constructor(
    private chessService: ChessService,
    private snackBar: MatSnackBar,
    private dialog: MatDialog
  ) {
    this.formats = [
      { value: 'bullet', viewValue: 'Bullet' },
      { value: 'blitz', viewValue: 'Blitz' },
      { value: 'rapid', viewValue: 'Rapid' },
    ]

    this.selectedFormat = this.formats[1].value;
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
      this.chessService.getGame(gameId).subscribe((result: ApiResult<ChessGameDto>) => {
        if (result.status == 200) {

          let data = result.data;
          this.game = new ChessGame(
            data.game_id,
            data.name,
            new GameFormat(data.game_format.value, data.game_format.remaining_time, data.game_format.additional_time),
            new Board(data.board),
            Side.parse(data.state.turn));

          this.game.setCheck(data.state.check_side, data.state.check_position);

          let that = this;

          data.history.forEach(function (value: HistoryEntryDto) {
            let piece = PieceFactory.getPiece(value.piece);

            that.game.history.push(new Movement(that.game.id, piece, value.from, value.to));
          });

          this.gameTimer = setInterval(function () {
            let whiteTimer = document.getElementById('timer1');
            let blackTimer = document.getElementById('timer2');

            if (whiteTimer) {
              whiteTimer.innerText = that.formatSeconds(that.game.whiteTimer);
            }

            if (blackTimer) {
              blackTimer.innerText = that.formatSeconds(that.game.blackTimer);
            }

            that.game.timerTick();
          }, 1000);
        }
      });

      this.playService.getMessages().subscribe(data => {
        try {
          console.log('received message:', data);
          const event = GameEventFactory.fromRaw(data);
          if (!event) return;

          if (event instanceof PieceMoveFailedEvent && event.game_id === this.game.id) {
            console.warn('Move failed on server:', event.reason);
            this.game.rollbackMove();

            this.dialog.open(MoveFailureDialogComponent, {
              data: {
                reason: event.reason || 'Illegal move',
                from: event.from,
                to: event.to
              },
              width: '350px'
            });
          } else if (event instanceof PieceMovedEvent || event instanceof PieceCapturedEvent) {
            // Reset check state on any move; if a new check occurs, a king-checked event will follow
            this.game.clearCheck();
          } else if (event instanceof KingCheckedEvent || event instanceof KingCheckmatedEvent) {
            this.game.setCheck(event.side, event.position);
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
    new_game.additional = this.selectedTimeOption?.additional || '';
    new_game.format = this.selectedFormat;
    new_game.name = this.game.name;
    new_game.time = this.selectedTimeOption?.time || '';

    this.chessService.startGame(new_game).subscribe((result: ApiResult<ChessGameDto>) => {
      if (result.status == 200) {
        let gameId = result.data.game_id;

        this.router.navigate(['/play', gameId])
      }
    });
  }

  selectTime(option: GameTimeOption): void {
    this.selectedTimeOption = option;
  }

  clickBoard(square: Cell): void {
    if (!!this.selectedSquare) {
      this.selectedSquare.selected = false;

      if (!!this.selectedSquare.piece) {
        if (this.game.movePiece(this.selectedSquare, square)) {
          let historyEntry = this.game.history.at(-1);

          this.playService.sendMessage(historyEntry);
        }
      }

      this.selectedSquare = null;

    } else {
      // Don't allow selecting a square if its piece doesn't follow turn 
      // and if the king is checked and not desired king's square is selected
      if (!square.piece) return;

      const isCorrectTurn = square.piece.side.value === this.game.turn.value;
      if (!isCorrectTurn) return;

      const isSideInCheck = this.game.checkSide === this.game.turn.value;
      if (isSideInCheck) {
        const isKingSelected = square.id === this.game.checkPosition?.toLowerCase();
        if (!isKingSelected) return;
      }

      square.selected = true;
      this.selectedSquare = square;
    }
  }

  updateBoardCheckState(): void {
    if (!this.game) return;

    this.game.board.flatBoard.forEach(cell => {
      cell.checked = !cell.isHeader && !!this.game.checkPosition && cell.id === this.game.checkPosition.toLowerCase();
    });
  }
}