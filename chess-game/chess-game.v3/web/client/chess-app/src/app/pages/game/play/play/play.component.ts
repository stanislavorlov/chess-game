import { Component, ElementRef, inject, OnInit, Renderer2, ViewChild } from '@angular/core';
import { MatSelectModule } from '@angular/material/select';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatRadioModule } from '@angular/material/radio';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { GroupedPosition, Position } from './models/position';
import { NgFor, NgIf } from '@angular/common';
import { ChessService } from 'src/app/services/chess.service';
import { GameFormat } from './models/game-format';
import { CreateGame } from './models/create-game';
import { ChessGame } from 'src/app/services/models/chess-game';
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

  //date: Date;
  //now: number;
  //difference: number;
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

  ngOnInit(): void {
    const gameId = this.route.snapshot.paramMap.get('id');
    
    if (!!gameId) {
      // ToDo: initialize existing game
      // ToDo: make read-only view

      this.chessService.getGame(gameId).subscribe((result: ApiResult<ChessGame>) => {
        if (result.status == 200) {
          this.game = result.data;
          this.gameName = this.game.name;

          console.log('loading game');
          console.log(this.game);

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

  positions: GroupedPosition[] = [
    { key: '8', group: [
      { square: 'a8', piece: 'br', color: 'light' },
      { square: 'b8', piece: 'bn', color: 'dark' },
      { square: 'c8', piece: 'bb', color: 'light' },
      { square: 'd8', piece: 'bq', color: 'dark' },
      { square: 'e8', piece: 'bk', color: 'light' },
      { square: 'f8', piece: 'bb', color: 'dark' },
      { square: 'g8', piece: 'bn', color: 'light' },
      { square: 'h8', piece: 'br', color: 'dark' },] },
    { key: '7', group: [
      { square: 'a7', piece: 'bp', color: 'dark' },
      { square: 'b7', piece: 'bp', color: 'light' },
      { square: 'c7', piece: 'bp', color: 'dark' },
      { square: 'd7', piece: 'bp', color: 'light' },
      { square: 'e7', piece: 'bp', color: 'dark' },
      { square: 'f7', piece: 'bp', color: 'light' },
      { square: 'g7', piece: 'bp', color: 'dark' },
      { square: 'h7', piece: 'bp', color: 'light' },] },
    { key: '6', group: [
      { square: 'a6', piece: '', color: 'light' },
      { square: 'b6', piece: '', color: 'dark' },
      { square: 'c6', piece: '', color: 'light' },
      { square: 'd6', piece: '', color: 'dark' },
      { square: 'e6', piece: '', color: 'light' },
      { square: 'f6', piece: '', color: 'dark' },
      { square: 'g6', piece: '', color: 'light' },
      { square: 'h6', piece: '', color: 'dark' },] },
    { key: '5', group: [
      { square: 'a5', piece: '', color: 'dark' },
      { square: 'b5', piece: '', color: 'light' },
      { square: 'c5', piece: '', color: 'dark' },
      { square: 'd5', piece: '', color: 'light' },
      { square: 'e5', piece: '', color: 'dark' },
      { square: 'f5', piece: '', color: 'light' },
      { square: 'g5', piece: '', color: 'dark' },
      { square: 'h5', piece: '', color: 'light' },] },
    { key: '4', group: [
      { square: 'a4', piece: '', color: 'light' },
      { square: 'b4', piece: '', color: 'dark' },
      { square: 'c4', piece: '', color: 'light' },
      { square: 'd4', piece: '', color: 'dark' },
      { square: 'e4', piece: '', color: 'light' },
      { square: 'f4', piece: '', color: 'dark' },
      { square: 'g4', piece: '', color: 'light' },
      { square: 'h4', piece: '', color: 'dark' },] },
    { key: '3', group: [
      { square: 'a3', piece: '', color: 'dark' },
      { square: 'b3', piece: '', color: 'light' },
      { square: 'c3', piece: '', color: 'dark' },
      { square: 'd3', piece: '', color: 'light' },
      { square: 'e3', piece: '', color: 'dark' },
      { square: 'f3', piece: '', color: 'light' },
      { square: 'g3', piece: '', color: 'dark' },
      { square: 'h3', piece: '', color: 'light' },] },
    { key: '2', group: [
      { square: 'a2', piece: 'wp', color: 'light' },
      { square: 'b2', piece: 'wp', color: 'dark' },
      { square: 'c2', piece: 'wp', color: 'light' },
      { square: 'd2', piece: 'wp', color: 'dark' },
      { square: 'e2', piece: 'wp', color: 'light' },
      { square: 'f2', piece: 'wp', color: 'dark' },
      { square: 'g2', piece: 'wp', color: 'light' },
      { square: 'h2', piece: 'wp', color: 'dark' },] },
    { key: '1', group: [
      { square: 'a1', piece: 'wr', color: 'dark' },
      { square: 'b1', piece: 'wn', color: 'light' },
      { square: 'c1', piece: 'wb', color: 'dark' },
      { square: 'd1', piece: 'wq', color: 'light' },
      { square: 'e1', piece: 'wk', color: 'dark' },
      { square: 'f1', piece: 'wb', color: 'light' },
      { square: 'g1', piece: 'wn', color: 'dark' },
      { square: 'h1', piece: 'wr', color: 'light' },] }
  ]

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

    this.playService.sendMessage('test message');
  }
}
