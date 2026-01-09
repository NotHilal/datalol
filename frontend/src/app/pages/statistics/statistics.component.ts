import { Component, OnInit } from '@angular/core';
import { StatisticsService } from '../../services/statistics.service';
import { ChampionService } from '../../services/champion.service';

@Component({
  selector: 'app-statistics',
  templateUrl: './statistics.component.html',
  styleUrls: ['./statistics.component.scss']
})
export class StatisticsComponent implements OnInit {
  allChampionStats: any[] = [];
  championStats: any[] = [];
  loading = true;

  championWinRateData: any;
  championPickRateData: any;
  championKDAData: any;

  // Filters
  selectedRole: string = 'All';
  selectedPosition: string = 'All';

  // Filter options
  roles: string[] = ['All', 'Tank', 'Fighter', 'Assassin', 'Mage', 'ADC', 'Support'];
  positions: string[] = ['All', 'TOP', 'JUNGLE', 'MIDDLE', 'BOTTOM', 'UTILITY'];

  constructor(
    private statisticsService: StatisticsService,
    public championService: ChampionService
  ) {}

  ngOnInit() {
    // Load champion roles first
    this.championService.getChampionRoles().subscribe({
      next: () => {
        this.loadStatistics();
      },
      error: () => {
        // Still try to load statistics even if roles fail
        this.loadStatistics();
      }
    });
  }

  loadStatistics() {
    this.loading = true;
    this.statisticsService.getChampionStatistics().subscribe({
      next: (statistics: any) => {
        // Enhance statistics with role information
        this.allChampionStats = statistics.map((stat: any) => ({
          ...stat,
          role: this.championService.getChampionRole(stat.champion)
        }));

        this.applyFilters();
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading statistics:', error);
        this.loading = false;
      }
    });
  }

  /**
   * Apply role and position filters
   */
  applyFilters() {
    let filtered = [...this.allChampionStats];

    // Filter by role
    if (this.selectedRole !== 'All') {
      filtered = filtered.filter(stat => stat.role === this.selectedRole);
    }

    // Filter by position (if position data is available in stats)
    if (this.selectedPosition !== 'All') {
      filtered = filtered.filter(stat => stat.position === this.selectedPosition);
    }

    this.championStats = filtered;
    this.prepareCharts();
  }

  /**
   * Handle role filter change
   */
  onRoleChange(role: string) {
    this.selectedRole = role;
    this.applyFilters();
  }

  /**
   * Handle position filter change
   */
  onPositionChange(position: string) {
    this.selectedPosition = position;
    this.applyFilters();
  }

  /**
   * Clear all filters
   */
  clearFilters() {
    this.selectedRole = 'All';
    this.selectedPosition = 'All';
    this.applyFilters();
  }

  /**
   * Get role color
   */
  getRoleColor(role: string): string {
    return this.championService.getRoleColor(role);
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
