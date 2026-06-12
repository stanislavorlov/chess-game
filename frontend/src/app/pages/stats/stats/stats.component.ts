import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../../../services/auth.service';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';

interface Match {
  id: string;
  type: string;
  value: number;
  light_player: string;
  dark_player: string;
  result: string;
  timestamp: string;
  outcome: 'win' | 'loss' | 'draw';
}

@Component({
  selector: 'app-stats',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatTableModule
  ],
  templateUrl: './stats.component.html',
  styleUrl: './stats.component.scss'
})
export class StatsComponent implements OnInit {
  matches: Match[] = [];
  userId: string | null = null;
  isGuest = false;

  // Stats summary
  totalPlayed = 0;
  wins = 0;
  losses = 0;
  draws = 0;

  winRate = 0;
  lossRate = 0;
  drawRate = 0;

  displayedColumns: string[] = ['index', 'opponent', 'outcome', 'date'];

  constructor(private http: HttpClient, private authService: AuthService) {}

  ngOnInit(): void {
    this.isGuest = this.authService.isGuest;
    const user = this.authService.currentUserValue;
    if (user && user._id) {
      this.userId = user._id;
      this.loadStats(user._id);
    }
  }

  loadStats(playerId: string): void {
    this.http.get<Match[]>(`/api/stats/player/${playerId}`).subscribe({
      next: (data) => {
        this.matches = data || [];
        this.calculateStats();
      },
      error: (err) => {
        console.error('Failed to load stats', err);
      }
    });
  }

  calculateStats(): void {
    this.totalPlayed = this.matches.length;
    if (this.totalPlayed === 0) return;

    this.wins = this.matches.filter(m => m.outcome === 'win').length;
    this.losses = this.matches.filter(m => m.outcome === 'loss').length;
    this.draws = this.matches.filter(m => m.outcome === 'draw').length;

    this.winRate = Math.round((this.wins / this.totalPlayed) * 100);
    this.lossRate = Math.round((this.losses / this.totalPlayed) * 100);
    this.drawRate = Math.round((this.draws / this.totalPlayed) * 100);
  }

  getOpponent(match: Match): string {
    const isLight = match.light_player === this.userId;
    const opp = isLight ? match.dark_player : match.light_player;
    return opp === "" ? "Computer" : opp;
  }
}

