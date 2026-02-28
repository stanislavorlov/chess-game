import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';

export interface GameOverData {
    result: string;
    finished_date?: string;
}

@Component({
    selector: 'app-game-over-dialog',
    standalone: true,
    imports: [MatDialogModule, MatButtonModule],
    template: `
    <h2 mat-dialog-title class="game-over-title">Game Over</h2>
    <mat-dialog-content>
      <div class="result-box">
        <h3 class="result-text">{{ data.result }}</h3>
      </div>
    </mat-dialog-content>
    <mat-dialog-actions align="center">
      <button mat-flat-button color="primary" mat-dialog-close>Close</button>
    </mat-dialog-actions>
  `,
    styles: [`
    .game-over-title {
      font-weight: bold;
      text-align: center;
      margin-bottom: 0;
    }
    .result-box {
      margin-top: 15px;
      padding: 15px;
      background-color: #f5f5f5;
      border-radius: 8px;
      text-align: center;
      min-width: 250px;
    }
    .result-text {
      margin: 0;
      color: #333;
      font-size: 1.5em;
    }
  `]
})
export class GameOverDialogComponent {
    constructor(
        @Inject(MAT_DIALOG_DATA) public data: GameOverData,
        public dialogRef: MatDialogRef<GameOverDialogComponent>
    ) { }
}
