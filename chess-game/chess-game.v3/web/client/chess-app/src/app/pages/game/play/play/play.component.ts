import { Component, inject, OnDestroy, OnInit, Renderer2 } from '@angular/core';
import { MatSelectModule } from '@angular/material/select';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatRadioModule } from '@angular/material/radio';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { NgFor, NgIf } from '@angular/common';
import { ChessService } from 'src/app/services/chess.service';
import { CreateGame } from './models/create-game';
import { ChessGameDto } from 'src/app/services/models/chess-game-dto';
import { ApiResult } from 'src/app/services/models/api-result';
import { ActivatedRoute, Router } from '@angular/router';
import { PlayService } from 'src/app/services/play.service';
import { ChessGame, GameFormat } from './models/game/chess-game';
import { Board } from 'src/app/pages/game/play/play/models/board/board';
import { TimeSelector } from './models/timeSelector';
import { Cell } from './models/board/ cell';

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
    NgFor, NgIf
  ],
  templateUrl: './play.component.html',
  styleUrl: './play.component.scss'
})
export class PlayComponent implements OnInit, OnDestroy {
  private lastClickedElement: HTMLElement | null = null;
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private selectedSquare: Cell | null = null;
  private secondsRemaining1: number;
  private secondsRemaining2: number;
  private switchPlayer: boolean = true;

  public formats: TimeSelector[];
  public selectedFormat = '';
  public selectedTime = '';
  public additionalTime = '';
  public game: ChessGame;

  constructor(private renderer: Renderer2, private chessService: ChessService, private playService: PlayService) {
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
      this.chessService.getGame(gameId).subscribe((result: ApiResult<ChessGameDto>) => {
        if (result.status == 200) {

          let data = result.data;
          this.game = new ChessGame(
            data.game_id,
            data.name, 
            new GameFormat(data.game_format.value, data.game_format.remaining_time, data.game_format.additional_time),
            new Board(data.board));

          let that = this;

          this.secondsRemaining1 = this.game.format.remaining;
          this.secondsRemaining2 = this.game.format.remaining;

          let timerId1 = setInterval(function() {
            if (that.switchPlayer) {
              let time1 = document.getElementById('timer1');

              if (time1) {
                time1.innerText = that.formatSeconds(that.secondsRemaining1)
                that.secondsRemaining1 -= 1;
              }
            } else {
              let time2 = document.getElementById('timer2');

              if (time2) {
                time2.innerText = that.formatSeconds(that.secondsRemaining2)
                that.secondsRemaining2 -= 1;
              }
            }
          }, 1000);
        }
      });

      this.playService.getMessages().subscribe(data => {
        console.log(data);
      });
    } else {
      this.game = this.chessService.newGame();
    }
  }

  ngOnDestroy(): void {
  }

  startGame(): void {
    const new_game = new CreateGame();
    new_game.additional = this.additionalTime;
    new_game.format = this.selectedFormat;
    new_game.name = this.game.name;
    new_game.time = this.selectedTime;

    this.chessService.startGame(new_game).subscribe((result: ApiResult<ChessGameDto>) => {
      if (result.status == 200) {
        let gameId = result.data.game_id;

        this.router.navigate(['/play', gameId ])
      }
    });
  }

  selectTime(event: Event, time: string, additional: string): void {
    let clickedElement = event.target as HTMLElement;

    if (clickedElement.tagName == 'span') {
      clickedElement = clickedElement.parentElement || clickedElement;
    }

    // Remove border from the last clicked element
    if (this.lastClickedElement) {
      this.renderer.setStyle(this.lastClickedElement, 'border', 'none');
    }

    // Add border to the clicked element
    this.renderer.setStyle(clickedElement, 'border', '2px solid red');

    // Update the last clicked element
    this.lastClickedElement = clickedElement;

    this.selectedTime = time;
    this.additionalTime = additional;
  }

  clickBoard(square: Cell): void {
    console.log(square);
    if (!!this.selectedSquare) {
      let fromElement = document.getElementById('cell-'+this.selectedSquare.id);
      fromElement?.style.setProperty('border', 'none','');

      if (!!this.selectedSquare.piece) {
        if (this.game.movePiece(this.selectedSquare, square)) {
          this.switchPlayer = !this.switchPlayer;

          let historyEntry = this.game.history.at(-1);

          this.playService.sendMessage(historyEntry);
        }
      }

      this.selectedSquare = null;
    } else {
      let htmlElement = document.getElementById('cell-'+square.id);
      htmlElement?.style.setProperty('border','1px solid red','');
      this.selectedSquare = square;
    }
  }
}