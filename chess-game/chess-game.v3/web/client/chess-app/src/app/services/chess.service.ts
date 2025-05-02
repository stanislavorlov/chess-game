import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { throwError } from 'rxjs';
import { CreateGame } from '../pages/game/play/play/models/create-game';
import { ChessGameDto } from './models/chess-game-dto';
import { ApiResult } from './models/api-result';
import { Board } from '../pages/game/play/play/models/board/board';
import { ChessGame, GameFormat } from '../pages/game/play/play/models/game/chess-game';
import { Cell } from '../pages/game/play/play/models/board/ cell';

@Injectable({
  providedIn: 'root'
})
export class ChessService {

  constructor(private httpClient: HttpClient) {

  }

  startGame(game: CreateGame) {
    return this.httpClient.post<ApiResult<ChessGameDto>>('/api/game/create_board/', {
      name: game.name,
      game_format: game.format,
      time: game.time,
      additional: game.additional
    }, {});
  }

  newGame() {
    let board = new Board([]);
    board.initialize();

    return new ChessGame('', 'Chess Game 1', new GameFormat('', 0, 0), board);
  }

  getGame(game_id: string) {
    return this.httpClient.get<ApiResult<ChessGameDto>>('/api/game/board/' + game_id);
  }

  validateMovement(from: Cell, to: Cell, board: Board) {
    /*let chess_board = new Board(board);
    
    if (chess_board.isValidMove(from, to)) {
        return true;
    }*/

    return board.isValidMove(from, to);
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
