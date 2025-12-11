export interface ChampionStatistics {
  champion: string;
  totalGames: number;
  wins: number;
  winRate: number;
  avgKills: number;
  avgDeaths: number;
  avgAssists: number;
  avgKDA: number;
  avgGold: number;
  avgDamage: number;
  avgCS: number;
}

export interface TeamStatistics {
  teamId: number;
  side: string;
  totalGames: number;
  wins: number;
  winRate: number;
}

export interface OverviewStatistics {
  totalMatches: number;
  teamStatistics: TeamStatistics[];
  topChampions: ChampionStatistics[];
}
