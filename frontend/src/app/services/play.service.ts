import { Injectable } from '@angular/core';
import { WebSocketSubject, webSocket } from 'rxjs/webSocket';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PlayService {

  private socket$!: WebSocketSubject<unknown>;

  constructor() { }

  setGameId(game_id: string) {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    this.socket$ = webSocket(`${protocol}//${host}/ws/${game_id}`);
  }

  // Send a message to the server
  sendMessage(message: unknown) {
    this.socket$.next(message);
  }

  // Receive messages from the server
  getMessages(): Observable<unknown> {
    return this.socket$.asObservable();
  }

  // Close the WebSocket connection
  closeConnection() {
    this.socket$.complete();
  }
}
