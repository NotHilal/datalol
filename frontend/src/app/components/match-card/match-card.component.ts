import { Component, Input, OnInit } from '@angular/core';
import { Match } from '../../models/match.model';
import { ChampionService } from '../../services/champion.service';

@Component({
  selector: 'app-match-card',
  templateUrl: './match-card.component.html',
  styleUrls: ['./match-card.component.scss']
})
export class MatchCardComponent implements OnInit {
  @Input() match!: Match;

  constructor(public championService: ChampionService) {}

  ngOnInit() {
    // Ensure champion roles are loaded
    this.championService.getChampionRoles().subscribe();
  }

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

  /**
   * Get team participants sorted by position
   */
  getTeamParticipants(teamId: number): any[] {
    const participants = this.match.participants.filter(p => p.position.teamId === teamId);

    // Sort by position order: TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY
    const positionOrder: { [key: string]: number } = {
      'TOP': 1,
      'JUNGLE': 2,
      'MIDDLE': 3,
      'BOTTOM': 4,
      'UTILITY': 5
    };

    return participants.sort((a, b) => {
      const orderA = positionOrder[a.position.teamPosition] || 999;
      const orderB = positionOrder[b.position.teamPosition] || 999;
      return orderA - orderB;
    });
  }

  /**
   * Get champion role/class
   */
  getChampionRole(championName: string): string {
    return this.championService.getChampionRole(championName);
  }

  /**
   * Get role color
   */
  getRoleColor(role: string): string {
    return this.championService.getRoleColor(role);
  }

  /**
   * Get position icon
   */
  getPositionIcon(position: string): string {
    return this.championService.getPositionIcon(position);
  }
}
