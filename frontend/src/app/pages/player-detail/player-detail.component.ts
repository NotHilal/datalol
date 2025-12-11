import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { PlayerService } from '../../services/player.service';
import { StatisticsService } from '../../services/statistics.service';

@Component({
  selector: 'app-player-detail',
  templateUrl: './player-detail.component.html',
  styleUrls: ['./player-detail.component.scss']
})
export class PlayerDetailComponent implements OnInit {
  playerStats: any = null;
  playerInfo: any = null;
  loading = true;
  playerPuuid: string = '';
  playerName: string = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private playerService: PlayerService,
    private statisticsService: StatisticsService
  ) {}

  ngOnInit() {
    this.route.params.subscribe(params => {
      this.playerPuuid = params['puuid'];
      this.loadPlayerData();
    });
  }

  loadPlayerData() {
    this.loading = true;
    // First, get player info including name
    this.playerService.getPlayerByPuuid(this.playerPuuid).subscribe({
      next: (response: any) => {
        this.playerInfo = response;
        this.playerName = response.name;

        // Then load player statistics using the name
        if (this.playerName) {
          this.loadPlayerStats();
        } else {
          console.error('Player name not found');
          this.loading = false;
        }
      },
      error: (error) => {
        console.error('Error loading player info:', error);
        this.loading = false;
      }
    });
  }

  loadPlayerStats() {
    this.statisticsService.getPlayerStatistics(this.playerName).subscribe({
      next: (statistics: any) => {
        this.playerStats = statistics;
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading player stats:', error);
        this.loading = false;
      }
    });
  }

  goBack() {
    this.router.navigate(['/players']);
  }
}
