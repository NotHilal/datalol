import { Injectable } from '@angular/core';
import { Observable, map, of } from 'rxjs';
import { tap } from 'rxjs/operators';
import { ApiService } from './api.service';
import { CacheService } from './cache.service';

export interface ChampionRole {
  championName: string;
  role: string;
}

export interface RoleInfo {
  description: string;
  characteristics: string[];
  color: string;
}

export interface PositionMetadata {
  icon: string;
  fullName: string;
  color: string;
}

@Injectable({
  providedIn: 'root'
})
export class ChampionService {
  private championRoles: { [key: string]: string } | null = null;
  private roleInfo: { [key: string]: RoleInfo } | null = null;

  constructor(
    private api: ApiService,
    private cache: CacheService
  ) {
    // Pre-load champion roles on service init
    this.loadChampionRoles().subscribe();
  }

  /**
   * Get champion role mappings (cached permanently since they rarely change)
   */
  getChampionRoles(): Observable<{ [key: string]: string }> {
    if (this.championRoles) {
      return of(this.championRoles);
    }

    const cacheKey = 'champions:roles';
    const request$ = this.api.get<any>('/champions/roles').pipe(
      map(response => response.data.championRoles),
      tap(roles => {
        this.championRoles = roles;
        this.roleInfo = null; // Will be loaded with full data
      })
    );

    // Cache for 24 hours (roles rarely change)
    return this.cache.wrap(cacheKey, request$, 86400000);
  }

  /**
   * Get role information with descriptions and colors
   */
  getRoleInfo(): Observable<{ [key: string]: RoleInfo }> {
    if (this.roleInfo) {
      return of(this.roleInfo);
    }

    const cacheKey = 'champions:roleInfo';
    const request$ = this.api.get<any>('/champions/roles').pipe(
      map(response => {
        this.championRoles = response.data.championRoles;
        this.roleInfo = response.data.roleInfo;
        return response.data.roleInfo;
      })
    );

    return this.cache.wrap(cacheKey, request$, 86400000);
  }

  /**
   * Get role for a specific champion (synchronous if already loaded)
   */
  getChampionRole(championName: string): string {
    if (!this.championRoles) {
      console.warn('[ChampionService] Roles not loaded yet for:', championName);
      return 'Fighter';
    }

    // Try exact match first
    if (championName in this.championRoles) {
      return this.championRoles[championName];
    }

    // Try case-insensitive match (database might have different casing)
    const lowerName = championName.toLowerCase();
    const matchingKey = Object.keys(this.championRoles).find(
      key => key.toLowerCase() === lowerName
    );

    if (matchingKey) {
      console.log(`[ChampionService] Case mismatch: "${championName}" -> "${matchingKey}"`);
      return this.championRoles[matchingKey];
    }

    console.warn(`[ChampionService] No role found for champion: "${championName}". Available keys:`, Object.keys(this.championRoles).slice(0, 5));
    return 'Fighter'; // Default fallback
  }

  /**
   * Get color for a role
   */
  getRoleColor(role: string): string {
    const colors: { [key: string]: string } = {
      'Tank': '#3498db',
      'Fighter': '#e74c3c',
      'Assassin': '#9b59b6',
      'Mage': '#1abc9c',
      'ADC': '#f39c12',
      'Support': '#2ecc71'
    };
    return colors[role] || '#95a5a6';
  }

  /**
   * Get all champion statistics with role information
   */
  getAllChampionStats(): Observable<any[]> {
    const cacheKey = 'champions:allStats';
    const request$ = this.api.get<any>('/champions/stats').pipe(
      map(response => response.data.champions)
    );

    // Cache for 10 minutes
    return this.cache.wrap(cacheKey, request$, 600000);
  }

  /**
   * Get position statistics (TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY)
   */
  getPositionStats(): Observable<any[]> {
    const cacheKey = 'champions:positionStats';
    const request$ = this.api.get<any>('/champions/positions').pipe(
      map(response => response.data.positions)
    );

    // Cache for 10 minutes
    return this.cache.wrap(cacheKey, request$, 600000);
  }

  /**
   * Get position icon emoji
   */
  getPositionIcon(position: string): string {
    const icons: { [key: string]: string } = {
      'TOP': '🛡️',
      'JUNGLE': '🌲',
      'MIDDLE': '⚡',
      'BOTTOM': '🎯',
      'UTILITY': '💚'
    };
    return icons[position] || '❓';
  }

  /**
   * Get position full name
   */
  getPositionName(position: string): string {
    const names: { [key: string]: string } = {
      'TOP': 'Top Lane',
      'JUNGLE': 'Jungle',
      'MIDDLE': 'Mid Lane',
      'BOTTOM': 'Bot Lane',
      'UTILITY': 'Support'
    };
    return names[position] || position;
  }

  /**
   * Get position color
   */
  getPositionColor(position: string): string {
    const colors: { [key: string]: string } = {
      'TOP': '#3498db',
      'JUNGLE': '#27ae60',
      'MIDDLE': '#9b59b6',
      'BOTTOM': '#e74c3c',
      'UTILITY': '#2ecc71'
    };
    return colors[position] || '#95a5a6';
  }

  /**
   * Load champion roles (called on init)
   */
  private loadChampionRoles(): Observable<any> {
    return this.getChampionRoles();
  }
}
