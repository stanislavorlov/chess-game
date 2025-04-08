import { Component, ElementRef, inject, OnInit, Renderer2, ViewChild } from '@angular/core';
import { MatSelectModule } from '@angular/material/select';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatRadioModule } from '@angular/material/radio';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { Position } from './models/position';
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
  public formats: GameFormat[];
  public selectedFormat = '';
  public selectedTime = '';
  public additionalTime = '';
  gameName = 'New Game 1';

  future: Date;
  timeot: NodeJS.Timeout

  public game: ChessGame;

  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

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
      // ToDo: initialize existing game
      // ToDo: make read-only view

      this.chessService.getGame(gameId).subscribe((result: ApiResult<ChessGame>) => {
        if (result.status == 200) {
          console.log(this.game);

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
      })
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

  positions: Record<number, Square[]>
  ranks: Array<string>

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

  clickBoard(position: Position): void {
    console.log('clicked square: ' + position.square + ', selected piece: ' + position.piece)

    var htmlElement = document.getElementById('td-'+position.square);
    if (!!htmlElement) {
      htmlElement.style.setProperty('border','1px solid red','');
    }

    //this.playService.sendMessage('test message');
  }
}

const groupBy = <T, K extends keyof any>(arr: T[], key: (i: T) => K) =>
  arr.reduce((groups, item) => {
    (groups[key(item)] ||= []).push(item);
    return groups;
  }, {} as Record<K, T[]>);