import { Component, OnInit } from '@angular/core';
import { StatisticsService } from '../../services/statistics.service';
import { MatchService } from '../../services/match.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {
  loading = true;
  overviewStats: any = null;
  recentMatches: any[] = [];
  championStats: any[] = [];

  // Chart data
  winRateChartData: any;
  championChartData: any;
  teamSideChartData: any;

  constructor(
    private statisticsService: StatisticsService,
    private matchService: MatchService
  ) {}

  ngOnInit() {
    this.loadDashboardData();
  }

  loadDashboardData() {
    this.loading = true;

    // Load overview statistics
    this.statisticsService.getOverviewStatistics().subscribe({
      next: (overviewStats: any) => {
        this.overviewStats = overviewStats;
        this.prepareTeamSideChart();
        this.loading = false;
      },
      error: (error: any) => {
        console.error('Error loading overview:', error);
        this.loading = false;
      }
    });

    // Load recent matches
    this.matchService.getMatches(1, 5).subscribe({
      next: (response: any) => {
        this.recentMatches = response.items;
      },
      error: (error: any) => {
        console.error('Error loading matches:', error);
      }
    });

    // Load champion statistics
    this.statisticsService.getChampionStatistics().subscribe({
      next: (statistics: any) => {
        this.championStats = statistics.slice(0, 10);
        this.prepareChampionCharts();
      },
      error: (error: any) => {
        console.error('Error loading champion stats:', error);
      }
    });
  }

  prepareTeamSideChart() {
    if (!this.overviewStats?.teamStatistics) return;

    const teamStats = this.overviewStats.teamStatistics;
    const blueTeam = teamStats.find((t: any) => t.side === 'Blue');
    const redTeam = teamStats.find((t: any) => t.side === 'Red');

    this.teamSideChartData = {
      labels: ['Blue Side', 'Red Side'],
      datasets: [{
        label: 'Win Rate (%)',
        data: [
          blueTeam?.winRate || 0,
          redTeam?.winRate || 0
        ],
        backgroundColor: [
          'rgba(76, 140, 255, 0.8)',
          'rgba(255, 76, 76, 0.8)'
        ],
        borderColor: [
          'rgba(76, 140, 255, 1)',
          'rgba(255, 76, 76, 1)'
        ],
        borderWidth: 2
      }]
    };
  }

  prepareChampionCharts() {
    if (!this.championStats || this.championStats.length === 0) return;

    // Win Rate Chart
    this.winRateChartData = {
      labels: this.championStats.map(c => c.champion),
      datasets: [{
        label: 'Win Rate (%)',
        data: this.championStats.map(c => c.winRate),
        backgroundColor: 'rgba(0, 200, 83, 0.6)',
        borderColor: 'rgba(0, 200, 83, 1)',
        borderWidth: 2
      }]
    };

    // Champion Pick Rate Chart
    this.championChartData = {
      labels: this.championStats.map(c => c.champion),
      datasets: [
        {
          label: 'Total Games',
          data: this.championStats.map(c => c.totalGames),
          backgroundColor: 'rgba(0, 151, 230, 0.6)',
          borderColor: 'rgba(0, 151, 230, 1)',
          borderWidth: 2
        },
        {
          label: 'Wins',
          data: this.championStats.map(c => c.wins),
          backgroundColor: 'rgba(0, 200, 83, 0.6)',
          borderColor: 'rgba(0, 200, 83, 1)',
          borderWidth: 2
        }
      ]
    };
  }

  get totalMatches(): number {
    return this.overviewStats?.totalMatches || 0;
  }

  get avgGameDuration(): string {
    // Placeholder - would need to calculate from data
    return '28m 45s';
  }

  get topChampion(): string {
    return this.championStats[0]?.champion || 'Loading...';
  }

  get topChampionWinRate(): number {
    return this.championStats[0]?.winRate || 0;
  }
}
