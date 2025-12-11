import { Component, Input } from '@angular/core';
import { Match } from '../../models/match.model';

@Component({
  selector: 'app-match-card',
  templateUrl: './match-card.component.html',
  styleUrls: ['./match-card.component.scss']
})
export class MatchCardComponent {
  @Input() match!: Match;

  getWinningTeam(): any {
    return this.match.teams.find(team => team.win);
  }

  getLosingTeam(): any {
    return this.match.teams.find(team => !team.win);
  }

  getTeamSide(teamId: number): string {
    return teamId === 100 ? 'Blue' : 'Red';
  }

  getGameDuration(): string {
    const duration = this.match.timestamps.gameDuration;
    const minutes = Math.floor(duration / 60);
    const seconds = duration % 60;
    return `${minutes}m ${seconds}s`;
  }

  getGameDate(): Date {
    return new Date(this.match.timestamps.gameCreation);
  }

  getTeamKills(teamId: number): number {
    return this.match.participants
      .filter(p => p.position.teamId === teamId)
      .reduce((sum, p) => sum + p.kda.kills, 0);
  }

  getTeamGold(teamId: number): number {
    return this.match.participants
      .filter(p => p.position.teamId === teamId)
      .reduce((sum, p) => sum + p.gold.earned, 0);
  }
}
