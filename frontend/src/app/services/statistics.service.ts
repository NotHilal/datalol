import { Injectable } from '@angular/core';
import { Observable, map } from 'rxjs';
import { HttpParams } from '@angular/common/http';
import { ApiService } from './api.service';
import { ChampionStatistics, TeamStatistics, OverviewStatistics } from '../models/statistics.model';
import { PlayerStatistics } from '../models/player.model';

@Injectable({
  providedIn: 'root'
})
export class StatisticsService {
  constructor(private api: ApiService) {}

  getChampionStatistics(championName?: string): Observable<ChampionStatistics[]> {
    let params = new HttpParams();
    if (championName) {
      params = params.set('champion', championName);
    }

    return this.api.get<any>('/statistics/champions', params).pipe(
      map(response => response.data.statistics)
    );
  }

  getPlayerStatistics(playerName: string): Observable<PlayerStatistics> {
    return this.api.get<any>(`/statistics/player/${playerName}`).pipe(
      map(response => response.data.statistics)
    );
  }

  getTeamStatistics(): Observable<TeamStatistics[]> {
    return this.api.get<any>('/statistics/teams').pipe(
      map(response => response.data.statistics)
    );
  }

  getOverviewStatistics(): Observable<OverviewStatistics> {
    return this.api.get<any>('/statistics/overview').pipe(
      map(response => response.data.overview)
    );
  }
}
