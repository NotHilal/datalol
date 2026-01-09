import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ChampionService } from '../../services/champion.service';

interface ChampionCard {
  name: string;
  role: string;
  roleColor: string;
  stats?: {
    totalGames: number;
    winRate: number;
    avgKDA: number;
    avgGold: number;
  };
}

@Component({
  selector: 'app-champions',
  templateUrl: './champions.component.html',
  styleUrls: ['./champions.component.scss']
})
export class ChampionsComponent implements OnInit {
  allChampions: ChampionCard[] = [];
  filteredChampions: ChampionCard[] = [];
  loading = true;

  // Filters
  searchQuery: string = '';
  selectedRole: string = 'All';

  // Filter options
  roles: string[] = ['All', 'Tank', 'Fighter', 'Assassin', 'Mage', 'ADC', 'Support'];

  // View mode
  viewMode: 'grid' | 'list' = 'grid';

  // Sort
  sortBy: 'name' | 'games' | 'winRate' | 'kda' = 'name';
  sortDirection: 'asc' | 'desc' = 'asc';

  constructor(
    public championService: ChampionService,
    private router: Router
  ) {}

  ngOnInit() {
    this.loadChampions();
  }

  loadChampions() {
    this.loading = true;

    // Load champion roles and stats
    this.championService.getChampionRoles().subscribe({
      next: (roles) => {
        // Get all champion stats
        this.championService.getAllChampionStats().subscribe({
          next: (stats) => {
            // Create champion cards
            const championNames = Object.keys(roles);

            this.allChampions = championNames.map(name => {
              const role = roles[name];
              const championStat = stats.find((s: any) => s.champion === name);

              return {
                name,
                role,
                roleColor: this.championService.getRoleColor(role),
                stats: championStat ? {
                  totalGames: championStat.totalGames,
                  winRate: championStat.winRate,
                  avgKDA: championStat.avgKDA,
                  avgGold: championStat.avgGold
                } : undefined
              };
            });

            this.applyFilters();
            this.loading = false;
          },
          error: (error) => {
            console.error('Error loading champion stats:', error);
            this.loading = false;
          }
        });
      },
      error: (error) => {
        console.error('Error loading champion roles:', error);
        this.loading = false;
      }
    });
  }

  /**
   * Apply search and role filters
   */
  applyFilters() {
    let filtered = [...this.allChampions];

    // Search filter
    if (this.searchQuery.trim()) {
      const query = this.searchQuery.toLowerCase();
      filtered = filtered.filter(champ =>
        champ.name.toLowerCase().includes(query) ||
        champ.role.toLowerCase().includes(query)
      );
    }

    // Role filter
    if (this.selectedRole !== 'All') {
      filtered = filtered.filter(champ => champ.role === this.selectedRole);
    }

    // Sort
    filtered.sort((a, b) => {
      let comparison = 0;

      switch (this.sortBy) {
        case 'name':
          comparison = a.name.localeCompare(b.name);
          break;
        case 'games':
          comparison = (a.stats?.totalGames || 0) - (b.stats?.totalGames || 0);
          break;
        case 'winRate':
          comparison = (a.stats?.winRate || 0) - (b.stats?.winRate || 0);
          break;
        case 'kda':
          comparison = (a.stats?.avgKDA || 0) - (b.stats?.avgKDA || 0);
          break;
      }

      return this.sortDirection === 'asc' ? comparison : -comparison;
    });

    this.filteredChampions = filtered;
  }

  /**
   * Handle search input
   */
  onSearchChange(query: string) {
    this.searchQuery = query;
    this.applyFilters();
  }

  /**
   * Handle role filter change
   */
  onRoleChange(role: string) {
    this.selectedRole = role;
    this.applyFilters();
  }

  /**
   * Handle sort change
   */
  onSortChange(sortBy: 'name' | 'games' | 'winRate' | 'kda') {
    if (this.sortBy === sortBy) {
      // Toggle direction
      this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortBy = sortBy;
      this.sortDirection = 'desc'; // Default to descending for stats
    }
    this.applyFilters();
  }

  /**
   * Toggle view mode
   */
  toggleViewMode() {
    this.viewMode = this.viewMode === 'grid' ? 'list' : 'grid';
  }

  /**
   * Clear all filters
   */
  clearFilters() {
    this.searchQuery = '';
    this.selectedRole = 'All';
    this.applyFilters();
  }

  /**
   * Navigate to champion detail (future feature)
   */
  viewChampion(championName: string) {
    // TODO: Navigate to champion detail page
    console.log('View champion:', championName);
    // this.router.navigate(['/champions', championName]);
  }
}
