import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { throwError } from 'rxjs';
import { CreateGame } from '../pages/game/play/play/models/create-game';
import { ChessGame, Square } from './models/chess-game';
import { ApiResult } from './models/api-result';
import { PieceFactory } from '../pages/game/play/play/models/pieces/piece_factory';

@Injectable({
  providedIn: 'root'
})
export class ChessService {

  constructor(private httpClient: HttpClient) { }

  startGame(game: CreateGame) {
    return this.httpClient.post<ApiResult<ChessGame>>('/api/game/create_board/', {
      name: game.name,
      game_format: game.format,
      time: game.time,
      additional: game.additional
    }, {});
  }

  newGame() {
    let chessGame = new ChessGame();

    chessGame.board = [
      {
          "square": "a0",
          "piece": "wr",
          "color": "B",
          "rank": 1
      },
      {
          "square": "a1",
          "piece": "wp",
          "color": "W",
          "rank": 2
      },
      {
          "square": "a2",
          "piece": "",
          "color": "B",
          "rank": 3
      },
      {
          "square": "a3",
          "piece": "",
          "color": "W",
          "rank": 4
      },
      {
          "square": "a4",
          "piece": "",
          "color": "B",
          "rank": 5
      },
      {
          "square": "a5",
          "piece": "",
          "color": "W",
          "rank": 6
      },
      {
          "square": "a6",
          "piece": "bp",
          "color": "B",
          "rank": 7
      },
      {
          "square": "a7",
          "piece": "br",
          "color": "W",
          "rank": 8
      },
      {
          "square": "b0",
          "piece": "wn",
          "color": "W",
          "rank": 1
      },
      {
          "square": "b1",
          "piece": "wp",
          "color": "B",
          "rank": 2
      },
      {
          "square": "b2",
          "piece": "",
          "color": "W",
          "rank": 3
      },
      {
          "square": "b3",
          "piece": "",
          "color": "B",
          "rank": 4
      },
      {
          "square": "b4",
          "piece": "",
          "color": "W",
          "rank": 5
      },
      {
          "square": "b5",
          "piece": "",
          "color": "B",
          "rank": 6
      },
      {
          "square": "b6",
          "piece": "bp",
          "color": "W",
          "rank": 7
      },
      {
          "square": "b7",
          "piece": "bn",
          "color": "B",
          "rank": 8
      },
      {
          "square": "c0",
          "piece": "wb",
          "color": "B",
          "rank": 1
      },
      {
          "square": "c1",
          "piece": "wp",
          "color": "W",
          "rank": 2
      },
      {
          "square": "c2",
          "piece": "",
          "color": "B",
          "rank": 3
      },
      {
          "square": "c3",
          "piece": "",
          "color": "W",
          "rank": 4
      },
      {
          "square": "c4",
          "piece": "",
          "color": "B",
          "rank": 5
      },
      {
          "square": "c5",
          "piece": "",
          "color": "W",
          "rank": 6
      },
      {
          "square": "c6",
          "piece": "bp",
          "color": "B",
          "rank": 7
      },
      {
          "square": "c7",
          "piece": "bb",
          "color": "W",
          "rank": 8
      },
      {
          "square": "d0",
          "piece": "wq",
          "color": "W",
          "rank": 1
      },
      {
          "square": "d1",
          "piece": "wp",
          "color": "B",
          "rank": 2
      },
      {
          "square": "d2",
          "piece": "",
          "color": "W",
          "rank": 3
      },
      {
          "square": "d3",
          "piece": "",
          "color": "B",
          "rank": 4
      },
      {
          "square": "d4",
          "piece": "",
          "color": "W",
          "rank": 5
      },
      {
          "square": "d5",
          "piece": "",
          "color": "B",
          "rank": 6
      },
      {
          "square": "d6",
          "piece": "bp",
          "color": "W",
          "rank": 7
      },
      {
          "square": "d7",
          "piece": "bq",
          "color": "B",
          "rank": 8
      },
      {
          "square": "e0",
          "piece": "wk",
          "color": "B",
          "rank": 1
      },
      {
          "square": "e1",
          "piece": "wp",
          "color": "W",
          "rank": 2
      },
      {
          "square": "e2",
          "piece": "",
          "color": "B",
          "rank": 3
      },
      {
          "square": "e3",
          "piece": "",
          "color": "W",
          "rank": 4
      },
      {
          "square": "e4",
          "piece": "",
          "color": "B",
          "rank": 5
      },
      {
          "square": "e5",
          "piece": "",
          "color": "W",
          "rank": 6
      },
      {
          "square": "e6",
          "piece": "bp",
          "color": "B",
          "rank": 7
      },
      {
          "square": "e7",
          "piece": "bk",
          "color": "W",
          "rank": 8
      },
      {
          "square": "f0",
          "piece": "wb",
          "color": "W",
          "rank": 1
      },
      {
          "square": "f1",
          "piece": "wp",
          "color": "B",
          "rank": 2
      },
      {
          "square": "f2",
          "piece": "",
          "color": "W",
          "rank": 3
      },
      {
          "square": "f3",
          "piece": "",
          "color": "B",
          "rank": 4
      },
      {
          "square": "f4",
          "piece": "",
          "color": "W",
          "rank": 5
      },
      {
          "square": "f5",
          "piece": "",
          "color": "B",
          "rank": 6
      },
      {
          "square": "f6",
          "piece": "bp",
          "color": "W",
          "rank": 7
      },
      {
          "square": "f7",
          "piece": "bb",
          "color": "B",
          "rank": 8
      },
      {
          "square": "g0",
          "piece": "wn",
          "color": "B",
          "rank": 1
      },
      {
          "square": "g1",
          "piece": "wp",
          "color": "W",
          "rank": 2
      },
      {
          "square": "g2",
          "piece": "",
          "color": "B",
          "rank": 3
      },
      {
          "square": "g3",
          "piece": "",
          "color": "W",
          "rank": 4
      },
      {
          "square": "g4",
          "piece": "",
          "color": "B",
          "rank": 5
      },
      {
          "square": "g5",
          "piece": "",
          "color": "W",
          "rank": 6
      },
      {
          "square": "g6",
          "piece": "bp",
          "color": "B",
          "rank": 7
      },
      {
          "square": "g7",
          "piece": "bn",
          "color": "W",
          "rank": 8
      },
      {
          "square": "h0",
          "piece": "wr",
          "color": "W",
          "rank": 1
      },
      {
          "square": "h1",
          "piece": "wp",
          "color": "B",
          "rank": 2
      },
      {
          "square": "h2",
          "piece": "",
          "color": "W",
          "rank": 3
      },
      {
          "square": "h3",
          "piece": "",
          "color": "B",
          "rank": 4
      },
      {
          "square": "h4",
          "piece": "",
          "color": "W",
          "rank": 5
      },
      {
          "square": "h5",
          "piece": "",
          "color": "B",
          "rank": 6
      },
      {
          "square": "h6",
          "piece": "bp",
          "color": "W",
          "rank": 7
      },
      {
          "square": "h7",
          "piece": "br",
          "color": "B",
          "rank": 8
      }];

    return chessGame;
  }

  getGame(game_id: string) {
    return this.httpClient.get<ApiResult<ChessGame>>('/api/game/board/' + game_id);
  }

  movePiece(from: Square, to: Square) {
    let piece_acronym = from.piece
    let piece = PieceFactory.getPiece('', piece_acronym)

    return piece.validate_move(from, to);
  }

  private handleError(error: HttpErrorResponse) {
    if (error.status === 0) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong.
      console.error(
        `Backend returned code ${error.status}, body was: `, error.error);
    }
    // Return an observable with a user-facing error message.
    return throwError(() => new Error('Something bad happened; please try again later.'));
  }
}
