import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-player-stats',
  templateUrl: './player-stats.component.html',
  styleUrls: ['./player-stats.component.scss']
})
export class PlayerStatsComponent {
  @Input() stats: any;

  getKDA(): number {
    if (!this.stats) return 0;
    const { avgKills, avgDeaths, avgAssists } = this.stats;
    if (avgDeaths === 0) return avgKills + avgAssists;
    return (avgKills + avgAssists) / avgDeaths;
  }

  getWinRateColor(): string {
    if (!this.stats) return '#a09b8c';
    const winRate = this.stats.winRate || 0;
    if (winRate >= 55) return '#00c853';
    if (winRate >= 50) return '#ffd700';
    if (winRate >= 45) return '#ff9800';
    return '#d32f2f';
  }

  getKDAColor(): string {
    const kda = this.getKDA();
    if (kda >= 4) return '#00c853';
    if (kda >= 3) return '#4caf50';
    if (kda >= 2) return '#ff9800';
    return '#d32f2f';
  }

  formatNumber(num: number): string {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num?.toString() || '0';
  }
}
