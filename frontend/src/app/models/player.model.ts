export interface Player {
  _id?: string;
  tier: string;
  rank: string;
  puuid: string;
  leaguePoints: number;
  wins: number;
  losses: number;
  veteran: boolean;
  inactive: boolean;
  freshBlood: boolean;
}

export interface PlayerStatistics {
  playerName: string;
  totalGames: number;
  wins: number;
  losses: number;
  winRate: number;
  avgKills: number;
  avgDeaths: number;
  avgAssists: number;
  totalKills: number;
  totalDeaths: number;
  totalAssists: number;
  avgKDA: number;
  avgGold: number;
  avgDamage: number;
  avgCS: number;
  pentaKills: number;
  quadraKills: number;
  tripleKills: number;
  doubleKills: number;
}
