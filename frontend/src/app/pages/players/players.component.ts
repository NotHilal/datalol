import { Component, OnInit } from '@angular/core';
import { PlayerService } from '../../services/player.service';
import { StatisticsService } from '../../services/statistics.service';
import { trigger, transition, style, animate } from '@angular/animations';

@Component({
  selector: 'app-players',
  templateUrl: './players.component.html',
  styleUrls: ['./players.component.scss'],
  animations: [
    trigger('slideDown', [
      transition(':enter', [
        style({ height: '0', opacity: 0, overflow: 'hidden' }),
        animate('300ms ease-out', style({ height: '*', opacity: 1 }))
      ]),
      transition(':leave', [
        animate('200ms ease-in', style({ height: '0', opacity: 0 }))
      ])
    ])
  ]
})
export class PlayersComponent implements OnInit {
  players: any[] = [];
  loading = false;
  initialLoad = true;
  currentPage = 1;
  pageSize = 20;
  totalPlayers = 0;
  totalPages = 0;
  sortBy: string = 'rank'; // Default sort by rank

  availableTiers: string[] = ['CHALLENGER', 'MASTER', 'DIAMOND', 'EMERALD', 'PLATINUM'];
  selectedTiers: string[] = [];
  showFilters: boolean = false;

  // Modal state
  showModal: boolean = false;
  modalLoading: boolean = false;
  selectedPlayerInfo: any = null;
  selectedPlayerStats: any = null;

  constructor(
    private playerService: PlayerService,
    private statisticsService: StatisticsService
  ) {}

  ngOnInit() {
    this.loadPlayers();
  }

  loadPlayers() {
    this.loading = true;
    const tiersParam = this.selectedTiers.length > 0 ? this.selectedTiers.join(',') : undefined;
    this.playerService.getPlayers(this.currentPage, this.pageSize, undefined, undefined, this.sortBy, tiersParam).subscribe({
      next: (response: any) => {
        this.players = response.items;
        this.totalPlayers = response.pagination.total;
        this.totalPages = response.pagination.totalPages;
        this.loading = false;
        this.initialLoad = false;
      },
      error: (error) => {
        console.error('Error loading players:', error);
        this.loading = false;
        this.initialLoad = false;
      }
    });
  }

  changeSorting(sortBy: string) {
    this.sortBy = sortBy;
    this.currentPage = 1; // Reset to first page when changing sort
    this.loadPlayers();
  }

  toggleTier(tier: string) {
    const index = this.selectedTiers.indexOf(tier);
    if (index > -1) {
      this.selectedTiers.splice(index, 1);
    } else {
      this.selectedTiers.push(tier);
    }
    this.currentPage = 1; // Reset to first page when changing filter
    this.loadPlayers();
  }

  clearFilters() {
    this.selectedTiers = [];
    this.currentPage = 1;
    this.loadPlayers();
  }

  onPageChange(page: number) {
    this.currentPage = page;
    this.loadPlayers();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  getWinRate(player: any): number {
    const total = player.wins + player.losses;
    if (total === 0) return 0;
    return Math.round((player.wins / total) * 100);
  }

  getTierClass(tier: string): string {
    return tier?.toLowerCase() || 'unranked';
  }

  getWinRateClass(winRate: number): string {
    if (winRate >= 60) return 'high';
    if (winRate >= 50) return 'medium';
    return 'low';
  }

  viewPlayerDetail(puuid: string) {
    this.showModal = true;
    this.modalLoading = true;
    this.selectedPlayerInfo = null;
    this.selectedPlayerStats = null;

    // First, get player info including name
    this.playerService.getPlayerByPuuid(puuid).subscribe({
      next: (playerInfo: any) => {
        this.selectedPlayerInfo = playerInfo;

        // Then load player statistics using the name
        if (playerInfo.name) {
          this.statisticsService.getPlayerStatistics(playerInfo.name).subscribe({
            next: (stats: any) => {
              this.selectedPlayerStats = stats;
              this.modalLoading = false;
            },
            error: (error) => {
              console.error('Error loading player stats:', error);
              this.modalLoading = false;
            }
          });
        } else {
          console.error('Player name not found');
          this.modalLoading = false;
        }
      },
      error: (error) => {
        console.error('Error loading player info:', error);
        this.modalLoading = false;
      }
    });
  }

  closeModal() {
    this.showModal = false;
    this.selectedPlayerInfo = null;
    this.selectedPlayerStats = null;
  }
}
