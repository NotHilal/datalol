import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MatchService } from '../../services/match.service';

@Component({
  selector: 'app-match-detail',
  templateUrl: './match-detail.component.html',
  styleUrls: ['./match-detail.component.scss']
})
export class MatchDetailComponent implements OnInit {
  match: any = null;
  loading = true;
  matchId: string = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private matchService: MatchService
  ) {}

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.matchId = params['id'];
      this.loadMatchDetail();
    });
  }

  loadMatchDetail() {
    this.loading = true;
    this.matchService.getMatchById(this.matchId).subscribe({
      next: (match: any) => {
        this.match = match;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading match:', error);
        this.loading = false;
      }
    });
  }

  getTeam(teamId: number) {
    return this.match.teams.find((t: any) => t.teamId === teamId);
  }

  getTeamParticipants(teamId: number) {
    return this.match.participants.filter((p: any) => p.position.teamId === teamId);
  }

  getGameDuration(): string {
    if (!this.match) return '';
    const duration = this.match.timestamps.gameDuration;
    const minutes = Math.floor(duration / 60);
    const seconds = duration % 60;
    return `${minutes}m ${seconds}s`;
  }

  getGameDate(): Date {
    return new Date(this.match.timestamps.gameCreation);
  }

  goBack() {
    this.router.navigate(['/matches']);
  }

  calculateKDA(participant: any): number {
    const { kills, deaths, assists } = participant.kda;
    if (deaths === 0) return kills + assists;
    return (kills + assists) / deaths;
  }

  getKDAClass(kda: number): string {
    if (kda >= 4) return 'excellent';
    if (kda >= 3) return 'good';
    if (kda >= 2) return 'average';
    return 'poor';
  }
}
