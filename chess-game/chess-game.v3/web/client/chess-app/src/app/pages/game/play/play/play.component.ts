import { Component, ElementRef, inject, NgZone, OnDestroy, OnInit, Renderer2, ViewChild } from '@angular/core';
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
import { GameFormat } from './models/game-format';
import { CreateGame } from './models/create-game';
import { ChessGame, Square } from 'src/app/services/models/chess-game';
import { ApiResult } from 'src/app/services/models/api-result';
import { ActivatedRoute, Router } from '@angular/router';
import { PlayService } from 'src/app/services/play.service';

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
  private selectedSquare: Square | null = null;
  private secondsRemaining1: number;
  private secondsRemaining2: number;
  private switchPlayer: boolean = true;

  public formats: GameFormat[];
  public selectedFormat = '';
  public selectedTime = '';
  public additionalTime = '';
  public gameName = 'New Game 1';
  public positions: Record<number, Square[]>;
  public ranks: Array<string>;
  public game: ChessGame;

  time = 0;

  constructor(private renderer: Renderer2, private ngZone: NgZone, private chessService: ChessService, private playService: PlayService) {
    this.formats = [
      { value: 'bullet', viewValue: 'Bullet' },
      { value: 'blitz', viewValue: 'Blitz' },
      { value: 'rapid', viewValue: 'Rapid' },
    ]

    this.selectedFormat = this.formats[1].value;
  }

  convertToNumber(rank: any) {
    return Number(rank);
  }

  formatSeconds(totalSeconds: number): string {
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;

    return minutes.toString() + 'm ' + seconds.toString().padStart(2, '0') + 's';
  }

  ngOnInit(): void {
    const gameId = this.route.snapshot.paramMap.get('id');
    
    if (!!gameId) {
      this.chessService.getGame(gameId).subscribe((result: ApiResult<ChessGame>) => {
        if (result.status == 200) {
          this.game = result.data;
          this.gameName = this.game.name;

          this.positions = groupBy(this.game.board, square => square.rank);
          this.ranks = Object.keys(this.positions) as Array<string>;

          let that = this;

          this.secondsRemaining1 = this.game.game_format.remaining_time;
          this.secondsRemaining2 = this.game.game_format.remaining_time;

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

          //ToDo: WebWorker
          /*this.timeot = setInterval(() => {
            this.tickTock();
          }, 1000);*/
          

          // ToDo: should be 2 separate timers for players
          /*let worker = this.worker;
          this.ngZone.runOutsideAngular(() => {
            worker = new Worker(new URL('src/app/services/timer.worker', import.meta.url), {
              type: 'module'
            });
            worker.onmessage = ({ data }) => {
              this.time = data.time;
              //console.log(this.time);
              this.tickTock();
            };

            worker.postMessage({ command: 'start', interval: 1000 });
          });*/
        }
      });

      this.playService.getMessages().subscribe(data => {
        console.log(data);
      });
    } else {
      let newGame = this.chessService.newGame();

      this.positions = groupBy(newGame.board, square => square.rank);
      this.ranks = Object.keys(this.positions) as Array<string>;
    }

    this.playService.sendMessage('Hello WebSocket');
  }

  ngOnDestroy(): void {
    /*if (this.worker) {
      this.worker.postMessage({ command: 'stop' });
      this.worker.terminate();
    }*/
  }

  startGame(): void {
    const new_game = new CreateGame();
    new_game.additional = this.additionalTime;
    new_game.format = this.selectedFormat;
    new_game.name = this.gameName;
    new_game.time = this.selectedTime;

    this.chessService.startGame(new_game).subscribe((result: ApiResult<ChessGame>) => {
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

  clickBoard(square: Square): void {
    console.log('clicked square: ' + square.square + ', selected piece: ' + square.piece);

    if (!!this.selectedSquare) {
      let fromElement = document.getElementById('td-'+this.selectedSquare.square);
      fromElement?.style.setProperty('border', 'none','');

      if (!!this.selectedSquare.piece) {
        if (this.chessService.validateMovement(this.selectedSquare, square, this.game.board)) {
          square.piece = this.selectedSquare.piece;
          this.selectedSquare.piece = '';
          this.switchPlayer = !this.switchPlayer;
        }
      }

      this.selectedSquare = null;
    } else {
      let htmlElement = document.getElementById('td-'+square.square);
      htmlElement?.style.setProperty('border','1px solid red','');
      this.selectedSquare = square;
    }

    //this.playService.sendMessage('test message');
  }
}

const groupBy = <T, K extends keyof any>(arr: T[], key: (i: T) => K) =>
  arr.reduce((groups, item) => {
    (groups[key(item)] ||= []).push(item);
    return groups;
  }, {} as Record<K, T[]>);