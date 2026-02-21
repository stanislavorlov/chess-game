import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { NgIf } from '@angular/common';

export interface MoveFailureData {
  reason: string;
  from_?: string;
  to?: string;
}

@Component({
  selector: 'app-move-failure-dialog',
  standalone: true,
  imports: [MatDialogModule, MatButtonModule, NgIf],
  template: `
    <h2 mat-dialog-title class="error-title">Move Rejected</h2>
    <mat-dialog-content>
      <p>{{ data.reason }}</p>
      <div *ngIf="data.from_ && data.to" class="move-details">
        Attempted move: <strong>{{ data.from_ }} → {{ data.to }}</strong>
      </div>
    </mat-dialog-content>
    <mat-dialog-actions align="end">
      <button mat-flat-button color="warn" mat-dialog-close>Understood</button>
    </mat-dialog-actions>
  `,
  styles: [`
    .error-title {
      color: #f44336;
      font-weight: bold;
    }
    .move-details {
      margin-top: 15px;
      padding: 10px;
      background-color: #f5f5f5;
      border-radius: 4px;
      font-size: 0.9em;
    }
  `]
})
export class MoveFailureDialogComponent {
  constructor(
    @Inject(MAT_DIALOG_DATA) public data: MoveFailureData,
    public dialogRef: MatDialogRef<MoveFailureDialogComponent>
  ) { }
}
