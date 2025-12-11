import { Component, OnInit } from '@angular/core';
import { StatisticsService } from '../../services/statistics.service';

@Component({
  selector: 'app-statistics',
  templateUrl: './statistics.component.html',
  styleUrls: ['./statistics.component.scss']
})
export class StatisticsComponent implements OnInit {
  championStats: any[] = [];
  loading = true;

  championWinRateData: any;
  championPickRateData: any;
  championKDAData: any;

  constructor(private statisticsService: StatisticsService) {}

  ngOnInit() {
    this.loadStatistics();
  }

  loadStatistics() {
    this.loading = true;
    this.statisticsService.getChampionStatistics().subscribe({
      next: (statistics: any) => {
        this.championStats = statistics;
        this.prepareCharts();
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading statistics:', error);
        this.loading = false;
      }
    });
  }

  prepareCharts() {
    const top15 = this.championStats.slice(0, 15);

    // Win Rate Chart
    this.championWinRateData = {
      labels: top15.map(c => c.champion),
      datasets: [{
        label: 'Win Rate (%)',
        data: top15.map(c => c.winRate),
        backgroundColor: 'rgba(0, 200, 83, 0.6)',
        borderColor: 'rgba(0, 200, 83, 1)',
        borderWidth: 2
      }]
    };

    // Pick Rate (Total Games)
    this.championPickRateData = {
      labels: top15.map(c => c.champion),
      datasets: [{
        label: 'Total Games Played',
        data: top15.map(c => c.totalGames),
        backgroundColor: 'rgba(0, 151, 230, 0.6)',
        borderColor: 'rgba(0, 151, 230, 1)',
        borderWidth: 2
      }]
    };

    // Average KDA
    this.championKDAData = {
      labels: top15.map(c => c.champion),
      datasets: [{
        label: 'Average KDA',
        data: top15.map(c => c.avgKDA),
        backgroundColor: 'rgba(255, 193, 7, 0.6)',
        borderColor: 'rgba(255, 193, 7, 1)',
        borderWidth: 2
      }]
    };
  }
}
