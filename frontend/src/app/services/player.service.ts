import { Injectable } from '@angular/core';
import { Observable, map } from 'rxjs';
import { HttpParams } from '@angular/common/http';
import { ApiService } from './api.service';
import { Player, PlayerStatistics } from '../models/player.model';
import { PaginatedResponse } from './match.service';

@Injectable({
  providedIn: 'root'
})
export class PlayerService {
  constructor(private api: ApiService) {}

  getPlayers(page: number = 1, pageSize: number = 20, tier?: string, rank?: string, sortBy?: string, tiers?: string): Observable<PaginatedResponse<Player>> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('pageSize', pageSize.toString());

    if (tier) params = params.set('tier', tier);
    if (rank) params = params.set('rank', rank);
    if (sortBy) params = params.set('sortBy', sortBy);
    if (tiers) params = params.set('tiers', tiers);

    return this.api.get<any>('/players', params).pipe(
      map(response => ({
        items: response.data.players,
        pagination: response.data.pagination
      }))
    );
  }

  getPlayerByPuuid(puuid: string): Observable<Player> {
    return this.api.get<any>(`/players/${puuid}`).pipe(
      map(response => response.data.player)
    );
  }

  getLeaderboard(limit: number = 100): Observable<Player[]> {
    const params = new HttpParams().set('limit', limit.toString());

    return this.api.get<any>('/players/leaderboard', params).pipe(
      map(response => response.data.leaderboard)
    );
  }

  getTierDistribution(): Observable<any[]> {
    return this.api.get<any>('/players/tier-distribution').pipe(
      map(response => response.data.distribution)
    );
  }
}
