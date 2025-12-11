import { Injectable } from '@angular/core';
import { Observable, map } from 'rxjs';
import { HttpParams } from '@angular/common/http';
import { ApiService, ApiResponse } from './api.service';
import { Match } from '../models/match.model';

export interface PaginatedResponse<T> {
  items: T[];
  pagination: {
    page: number;
    pageSize: number;
    total: number;
    totalPages: number;
  };
}

@Injectable({
  providedIn: 'root'
})
export class MatchService {
  constructor(private api: ApiService) {}

  getMatches(page: number = 1, pageSize: number = 20): Observable<PaginatedResponse<Match>> {
    const params = new HttpParams()
      .set('page', page.toString())
      .set('pageSize', pageSize.toString());

    return this.api.get<any>('/matches', params).pipe(
      map(response => ({
        items: response.data.matches,
        pagination: response.data.pagination
      }))
    );
  }

  getMatchById(matchId: string): Observable<Match> {
    return this.api.get<any>(`/matches/${matchId}`).pipe(
      map(response => response.data.match)
    );
  }

  getMatchesByPlayer(playerName: string, page: number = 1, pageSize: number = 20): Observable<PaginatedResponse<Match>> {
    const params = new HttpParams()
      .set('page', page.toString())
      .set('pageSize', pageSize.toString());

    return this.api.get<any>(`/matches/player/${playerName}`, params).pipe(
      map(response => ({
        items: response.data.matches,
        pagination: response.data.pagination
      }))
    );
  }

  getMatchesByChampion(championName: string, page: number = 1, pageSize: number = 20): Observable<PaginatedResponse<Match>> {
    const params = new HttpParams()
      .set('page', page.toString())
      .set('pageSize', pageSize.toString());

    return this.api.get<any>(`/matches/champion/${championName}`, params).pipe(
      map(response => ({
        items: response.data.matches,
        pagination: response.data.pagination
      }))
    );
  }
}
