# API Documentation

## Base URL
```
http://localhost:5000/api/v1
```

## Response Format

All API endpoints return responses in the following format:

### Success Response
```json
{
  "success": true,
  "data": {
    // Response data here
  }
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "message": "Error message here",
    "code": 400
  }
}
```

---

## Matches Endpoints

### GET /matches
Get all matches with pagination.

**Query Parameters:**
- `page` (number, optional): Page number (default: 1)
- `pageSize` (number, optional): Items per page (default: 20, max: 100)

**Example Request:**
```
GET /api/v1/matches?page=1&pageSize=20
```

**Response:**
```json
{
  "success": true,
  "data": {
    "matches": [...],
    "pagination": {
      "page": 1,
      "pageSize": 20,
      "total": 101843,
      "totalPages": 5093
    }
  }
}
```

---

### GET /matches/:matchId
Get a specific match by ID.

**URL Parameters:**
- `matchId` (string): Match ID (e.g., "NA1_5348438296")

**Example Request:**
```
GET /api/v1/matches/NA1_5348438296
```

**Response:**
```json
{
  "success": true,
  "data": {
    "match": {
      "matchId": "NA1_5348438296",
      "gameInfo": {
        "gameMode": "CLASSIC",
        "gameDuration": 1682,
        ...
      },
      "teams": [...],
      "participants": [...]
    }
  }
}
```

---

### GET /matches/player/:playerName
Get all matches for a specific player.

**URL Parameters:**
- `playerName` (string): Player's Riot ID game name

**Query Parameters:**
- `page` (number, optional): Page number (default: 1)
- `pageSize` (number, optional): Items per page (default: 20)

**Example Request:**
```
GET /api/v1/matches/player/EcigaretteDz?page=1&pageSize=20
```

**Response:**
```json
{
  "success": true,
  "data": {
    "player": "EcigaretteDz",
    "matches": [...],
    "pagination": {
      "page": 1,
      "pageSize": 20,
      "total": 45,
      "totalPages": 3
    }
  }
}
```

---

### GET /matches/champion/:championName
Get all matches featuring a specific champion.

**URL Parameters:**
- `championName` (string): Champion name (e.g., "Teemo", "Sylas")

**Query Parameters:**
- `page` (number, optional): Page number (default: 1)
- `pageSize` (number, optional): Items per page (default: 20)

**Example Request:**
```
GET /api/v1/matches/champion/Teemo?page=1&pageSize=20
```

**Response:**
```json
{
  "success": true,
  "data": {
    "champion": "Teemo",
    "matches": [...],
    "pagination": {
      "page": 1,
      "pageSize": 20,
      "total": 1250,
      "totalPages": 63
    }
  }
}
```

---

## Players Endpoints

### GET /players
Get all players with pagination and optional filters.

**Query Parameters:**
- `page` (number, optional): Page number (default: 1)
- `pageSize` (number, optional): Items per page (default: 20)
- `tier` (string, optional): Filter by tier (PLATINUM, EMERALD, etc.)
- `rank` (string, optional): Filter by rank (I, II, III, IV)

**Example Request:**
```
GET /api/v1/players?tier=PLATINUM&rank=I&page=1&pageSize=20
```

**Response:**
```json
{
  "success": true,
  "data": {
    "players": [
      {
        "tier": "PLATINUM",
        "rank": "I",
        "puuid": "CEAj3J8Z...",
        "leaguePoints": 72,
        "wins": 106,
        "losses": 109,
        "veteran": false,
        "inactive": false,
        "freshBlood": false
      },
      ...
    ],
    "pagination": {
      "page": 1,
      "pageSize": 20,
      "total": 500,
      "totalPages": 25
    }
  }
}
```

---

### GET /players/:puuid
Get a specific player by PUUID.

**URL Parameters:**
- `puuid` (string): Player's PUUID

**Example Request:**
```
GET /api/v1/players/CEAj3J8ZSyHIHaARmGnWDbQJ34...
```

**Response:**
```json
{
  "success": true,
  "data": {
    "player": {
      "tier": "PLATINUM",
      "rank": "I",
      "puuid": "CEAj3J8Z...",
      "leaguePoints": 72,
      "wins": 106,
      "losses": 109,
      "veteran": false,
      "inactive": false,
      "freshBlood": false
    }
  }
}
```

---

### GET /players/leaderboard
Get top players leaderboard.

**Query Parameters:**
- `limit` (number, optional): Number of players to return (default: 100, max: 500)

**Example Request:**
```
GET /api/v1/players/leaderboard?limit=50
```

**Response:**
```json
{
  "success": true,
  "data": {
    "leaderboard": [...],
    "count": 50
  }
}
```

---

### GET /players/tier-distribution
Get distribution of players across tiers and ranks.

**Example Request:**
```
GET /api/v1/players/tier-distribution
```

**Response:**
```json
{
  "success": true,
  "data": {
    "distribution": [
      {
        "tier": "PLATINUM",
        "rank": "I",
        "playerCount": 450,
        "avgLP": 55.5,
        "avgWins": 98.2,
        "avgLosses": 95.8,
        "avgWinRate": 50.6
      },
      ...
    ]
  }
}
```

---

## Statistics Endpoints

### GET /statistics/champions
Get aggregated statistics for champions.

**Query Parameters:**
- `champion` (string, optional): Filter by specific champion name

**Example Request:**
```
GET /api/v1/statistics/champions
```

**Response:**
```json
{
  "success": true,
  "data": {
    "statistics": [
      {
        "champion": "Sylas",
        "totalGames": 5420,
        "wins": 2850,
        "winRate": 52.58,
        "avgKills": 7.2,
        "avgDeaths": 5.8,
        "avgAssists": 8.1,
        "avgKDA": 2.64,
        "avgGold": 11250,
        "avgDamage": 18500,
        "avgCS": 165.5
      },
      ...
    ],
    "count": 150
  }
}
```

---

### GET /statistics/player/:playerName
Get aggregated statistics for a specific player.

**URL Parameters:**
- `playerName` (string): Player's Riot ID game name

**Example Request:**
```
GET /api/v1/statistics/player/EcigaretteDz
```

**Response:**
```json
{
  "success": true,
  "data": {
    "statistics": {
      "playerName": "EcigaretteDz",
      "totalGames": 215,
      "wins": 118,
      "losses": 97,
      "winRate": 54.88,
      "avgKills": 6.5,
      "avgDeaths": 5.2,
      "avgAssists": 7.8,
      "totalKills": 1397,
      "totalDeaths": 1118,
      "totalAssists": 1677,
      "avgKDA": 2.73,
      "avgGold": 10850,
      "avgDamage": 17200,
      "avgCS": 158.3,
      "pentaKills": 2,
      "quadraKills": 8,
      "tripleKills": 25,
      "doubleKills": 87
    }
  }
}
```

---

### GET /statistics/teams
Get win rates by team side (Blue vs Red).

**Example Request:**
```
GET /api/v1/statistics/teams
```

**Response:**
```json
{
  "success": true,
  "data": {
    "statistics": [
      {
        "teamId": 100,
        "side": "Blue",
        "totalGames": 101843,
        "wins": 51420,
        "winRate": 50.49
      },
      {
        "teamId": 200,
        "side": "Red",
        "totalGames": 101843,
        "wins": 50423,
        "winRate": 49.51
      }
    ]
  }
}
```

---

### GET /statistics/overview
Get overall statistics overview.

**Example Request:**
```
GET /api/v1/statistics/overview
```

**Response:**
```json
{
  "success": true,
  "data": {
    "overview": {
      "totalMatches": 101843,
      "teamStatistics": [...],
      "topChampions": [...]
    }
  }
}
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

---

## Rate Limiting

Currently, there is no rate limiting implemented. This may be added in future versions.

---

## Data Models

### Match Object
```typescript
{
  matchId: string,
  gameInfo: {
    gameMode: string,
    gameDuration: number,
    gameVersion: string,
    mapId: number
  },
  timestamps: {
    gameCreation: number,
    gameEndTimestamp: number,
    gameDuration: number
  },
  teams: Team[],
  participants: Participant[]
}
```

### Participant Object
```typescript
{
  participantId: number,
  puuid: string,
  champion: {
    id: number,
    name: string,
    level: number
  },
  summoner: {
    riotIdGameName: string,
    riotIdTagline: string,
    summonerLevel: number
  },
  kda: {
    kills: number,
    deaths: number,
    assists: number
  },
  gold: {
    earned: number,
    spent: number
  },
  win: boolean
}
```

---

## Examples

### Using cURL

```bash
# Get matches
curl http://localhost:5000/api/v1/matches?page=1&pageSize=10

# Get specific match
curl http://localhost:5000/api/v1/matches/NA1_5348438296

# Get player statistics
curl http://localhost:5000/api/v1/statistics/player/EcigaretteDz

# Get champion statistics
curl http://localhost:5000/api/v1/statistics/champions?champion=Teemo
```

### Using JavaScript (Fetch API)

```javascript
// Get matches
fetch('http://localhost:5000/api/v1/matches?page=1&pageSize=20')
  .then(response => response.json())
  .then(data => console.log(data.data.matches));

// Get player statistics
fetch('http://localhost:5000/api/v1/statistics/player/EcigaretteDz')
  .then(response => response.json())
  .then(data => console.log(data.data.statistics));
```

---

## Support

For issues or questions, please create an issue in the project repository.
