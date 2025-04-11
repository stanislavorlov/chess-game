import { Component, ElementRef, inject, OnInit, Renderer2, ViewChild } from '@angular/core';
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
export class PlayComponent implements OnInit {
  private lastClickedElement: HTMLElement | null = null;
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private future: Date;
  private timeot: NodeJS.Timeout;
  private selectedSquare: Square | null = null;

  public formats: GameFormat[];
  public selectedFormat = '';
  public selectedTime = '';
  public additionalTime = '';
  public gameName = 'New Game 1';
  public positions: Record<number, Square[]>;
  public ranks: Array<string>;
  public game: ChessGame;

  @ViewChild('minutes', { static: true }) minutes: ElementRef<HTMLInputElement> = {} as ElementRef;
  @ViewChild('seconds', { static: true }) seconds: ElementRef<HTMLInputElement> = {} as ElementRef;

  constructor(private renderer: Renderer2, private chessService: ChessService, private playService: PlayService) {
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

  ngOnInit(): void {
    const gameId = this.route.snapshot.paramMap.get('id');
    
    if (!!gameId) {
      this.chessService.getGame(gameId).subscribe((result: ApiResult<ChessGame>) => {
        if (result.status == 200) {
          this.game = result.data;
          this.gameName = this.game.name;

          this.positions = groupBy(this.game.board, square => square.rank);
          this.ranks = Object.keys(this.positions) as Array<string>;

          let now: Date = new Date();
          this.future = new Date(now.getTime() + this.game.game_format.remaining_time * 1000);

          this.timeot = setInterval(() => {
            this.tickTock();
          }, 1000);
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

  tickTock() {
    let now = new Date();
    if (this.future > now) {
      let differefence = new Date(this.future.valueOf() - now.valueOf());
      // ToDo: bind variables instead of ref
      this.minutes.nativeElement.innerText = differefence.getMinutes().toString();
      this.seconds.nativeElement.innerText = differefence.getSeconds().toString();
    } else {
      clearInterval(this.timeot);
    }
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
        }
      }

      //let toElement = document.getElementById('td-'+square.square);
      //toElement?.style.setProperty('border','1px solid red','');

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