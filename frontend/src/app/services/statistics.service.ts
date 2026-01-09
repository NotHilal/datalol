import { Injectable } from '@angular/core';
import { Observable, map } from 'rxjs';
import { HttpParams } from '@angular/common/http';
import { ApiService } from './api.service';
import { CacheService } from './cache.service';
import { ChampionStatistics, TeamStatistics, OverviewStatistics } from '../models/statistics.model';
import { PlayerStatistics } from '../models/player.model';

@Injectable({
  providedIn: 'root'
})
export class StatisticsService {
  constructor(
    private api: ApiService,
    private cache: CacheService
  ) {}

  getChampionStatistics(championName?: string): Observable<ChampionStatistics[]> {
    let params = new HttpParams();
    if (championName) {
      params = params.set('champion', championName);
    }

    const cacheKey = `stats:champions:${championName || 'all'}`;
    const request$ = this.api.get<any>('/statistics/champions', params).pipe(
      map(response => response.data.statistics)
    );

    // Cache for 10 minutes (matches backend cache)
    return this.cache.wrap(cacheKey, request$, 600000);
  }

  getPlayerStatistics(playerName: string): Observable<PlayerStatistics> {
    const cacheKey = `stats:player:${playerName}`;
    const request$ = this.api.get<any>(`/statistics/player/${playerName}`).pipe(
      map(response => response.data.statistics)
    );

    // Cache for 5 minutes
    return this.cache.wrap(cacheKey, request$, 300000);
  }

  getTeamStatistics(): Observable<TeamStatistics[]> {
    const cacheKey = 'stats:teams';
    const request$ = this.api.get<any>('/statistics/teams').pipe(
      map(response => response.data.statistics)
    );

    // Cache for 30 minutes (team stats rarely change)
    return this.cache.wrap(cacheKey, request$, 1800000);
  }

  getOverviewStatistics(): Observable<OverviewStatistics> {
    const cacheKey = 'stats:overview';
    const request$ = this.api.get<any>('/statistics/overview').pipe(
      map(response => response.data.overview)
    );

    // Cache for 10 minutes
    return this.cache.wrap(cacheKey, request$, 600000);
  }
}
