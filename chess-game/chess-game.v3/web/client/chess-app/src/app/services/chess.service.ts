import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { throwError } from 'rxjs';
import { CreateGame } from '../pages/game/play/play/models/create-game';
import { ChessGame } from './models/chess-game';
import { ApiResult } from './models/api-result';

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
