export interface Match {
  _id?: string;
  matchId: string;
  dataVersion: string;
  gameInfo: GameInfo;
  timestamps: Timestamps;
  teams: Team[];
  participants: Participant[];
}

export interface GameInfo {
  gameId: number;
  gameMode: string;
  gameType: string;
  gameName: string;
  gameVersion: string;
  mapId: number;
  endOfGameResult: string;
}

export interface Timestamps {
  gameCreation: number;
  gameEndTimestamp: number;
  gameDuration: number;
}

export interface Team {
  teamId: number;
  win: boolean;
  bans: Ban[];
  objectives: TeamObjectives;
}

export interface Ban {
  championId: number;
  pickTurn: number;
}

export interface TeamObjectives {
  baron: ObjectiveInfo;
  dragon: ObjectiveInfo;
  tower: ObjectiveInfo;
  inhibitor: ObjectiveInfo;
  riftHerald: ObjectiveInfo;
}

export interface ObjectiveInfo {
  first: boolean;
  kills: number;
}

export interface Participant {
  participantId: number;
  puuid: string;
  champion: Champion;
  summoner: Summoner;
  position: Position;
  kda: KDA;
  damage: Damage;
  gold: Gold;
  items: number[];
  farming: Farming;
  objectives: ParticipantObjectives;
  vision: Vision;
  win: boolean;
}

export interface Champion {
  id: number;
  name: string;
  level: number;
  experience: number;
}

export interface Summoner {
  id: string;
  name: string;
  level: number;
  riotIdGameName: string;
  riotIdTagline: string;
  profileIcon: number;
}

export interface Position {
  teamId: number;
  teamPosition: string;
  individualPosition: string;
  lane: string;
  role: string;
}

export interface KDA {
  kills: number;
  deaths: number;
  assists: number;
  doubleKills: number;
  tripleKills: number;
  quadraKills: number;
  pentaKills: number;
}

export interface Damage {
  totalDealt: number;
  totalDealtToChampions: number;
  physicalDealt: number;
  magicDealt: number;
  trueDealt: number;
  totalTaken: number;
}

export interface Gold {
  earned: number;
  spent: number;
}

export interface Farming {
  totalMinionsKilled: number;
  neutralMinionsKilled: number;
  totalAllyJungleMinionsKilled: number;
  totalEnemyJungleMinionsKilled: number;
}

export interface ParticipantObjectives {
  baronKills: number;
  dragonKills: number;
  turretKills: number;
  inhibitorKills: number;
}

export interface Vision {
  visionScore: number;
  wardsPlaced: number;
  wardsKilled: number;
}
