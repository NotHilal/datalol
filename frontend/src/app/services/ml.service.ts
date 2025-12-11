import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiService, ApiResponse } from './api.service';

export interface ModelInfo {
  id: string;
  name: string;
  type: string;
  algorithm: string;
  accuracy?: number;
  rmse?: number;
  clusters?: number;
  description: string;
  available: boolean;
}

export interface MatchPrediction {
  prediction: string;
  predicted_value: number;
  confidence: number;
  probabilities: {
    red_team: number;
    blue_team: number;
  };
}

export interface DurationPrediction {
  predicted_duration_minutes: number;
  predicted_duration_formatted: string;
}

export interface SamplePredictionResult {
  matchId: string;
  predicted_winner: string;
  actual_winner: string;
  correct: boolean;
  confidence: number;
  gold_diff: number;
  tower_diff: number;
}

export interface DurationPredictionResult {
  matchId: string;
  predicted_duration: number;
  actual_duration: number;
  error_minutes: number;
  total_objectives: number;
  total_kills: number;
}

export interface SamplePredictions {
  match_predictions: SamplePredictionResult[];
  match_accuracy: number;
  duration_predictions: DurationPredictionResult[];
  avg_duration_error: number;
  sample_count: number;
}

export interface ChampionCluster {
  cluster_id: number;
  size: number;
  champions: Array<{
    champion: string;
    totalGames: number;
    winRate: number;
    avgKDA: number;
  }>;
}

export interface DraftPrediction {
  prediction: string;
  predicted_value: number;
  confidence: number;
  probabilities: {
    red_team: number;
    blue_team: number;
  };
  analysis: {
    blue_team_strength: number;
    red_team_strength: number;
    blue_avg_kda: number;
    red_avg_kda: number;
    win_rate_advantage: string;
    damage_advantage: string;
  };
  features?: {
    blue_team: TeamFeatures;
    red_team: TeamFeatures;
    differentials: DifferentialFeatures;
  };
}

export interface TeamFeatures {
  avg_win_rate: number;
  avg_kda: number;
  avg_kills: number;
  avg_deaths: number;
  avg_assists: number;
  avg_gold: number;
  avg_damage: number;
  avg_cs: number;
  total_games: number;
  min_win_rate: number;
  max_win_rate: number;
  win_rate_variance: number;
}

export interface DifferentialFeatures {
  win_rate_diff: number;
  kda_diff: number;
  damage_diff: number;
  gold_diff: number;
  cs_diff: number;
}

@Injectable({
  providedIn: 'root'
})
export class MlService {

  constructor(private apiService: ApiService) { }

  /**
   * Get information about available ML models
   */
  getModelsInfo(): Observable<any> {
    return this.apiService.get<any>('/ml/models/info').pipe(
      map(response => response.data)
    );
  }

  /**
   * Predict match outcome
   */
  predictMatchOutcome(matchData: any): Observable<MatchPrediction> {
    return this.apiService.post<MatchPrediction>('/ml/predict/match-outcome', matchData).pipe(
      map(response => response.data)
    );
  }

  /**
   * Predict match duration
   */
  predictDuration(matchData: any): Observable<DurationPrediction> {
    return this.apiService.post<DurationPrediction>('/ml/predict/duration', matchData).pipe(
      map(response => response.data)
    );
  }

  /**
   * Get sample predictions from database matches
   */
  getSamplePredictions(limit: number = 5): Observable<SamplePredictions> {
    return this.apiService.get<SamplePredictions>(`/ml/test/sample-predictions?limit=${limit}`).pipe(
      map(response => response.data)
    );
  }

  /**
   * Get list of available visualizations
   */
  getVisualizations(): Observable<any> {
    return this.apiService.get<any>('/ml/visualizations').pipe(
      map(response => response.data)
    );
  }

  /**
   * Get visualization image URL
   */
  getVisualizationUrl(filename: string): string {
    return `http://localhost:5000/api/v1/ml/visualizations/${filename}`;
  }

  /**
   * Get champion cluster information
   */
  getChampionClusters(): Observable<any> {
    return this.apiService.get<any>('/ml/champion-clusters').pipe(
      map(response => response.data)
    );
  }

  /**
   * Get list of all champions for draft selection
   */
  getChampions(): Observable<string[]> {
    return this.apiService.get<any>('/ml/champions').pipe(
      map(response => response.data.champions)
    );
  }

  /**
   * Predict match outcome based on champion draft (5v5)
   */
  predictDraft(blueTeam: string[], redTeam: string[]): Observable<DraftPrediction> {
    return this.apiService.post<DraftPrediction>('/ml/predict/draft', {
      blue_team: blueTeam,
      red_team: redTeam
    }).pipe(
      map(response => response.data)
    );
  }
}
