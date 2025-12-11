# Backend - Flask API

Flask REST API for League of Legends Match Analytics.

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Run Application

```bash
python run.py
```

The API will be available at `http://localhost:5000`

## Project Structure

```
backend/
├── app/
│   ├── models/           # Database models
│   │   ├── match.py     # Match model with aggregation queries
│   │   └── player.py    # Player model
│   ├── routes/          # API endpoints
│   │   ├── matches.py   # Match routes
│   │   ├── players.py   # Player routes
│   │   └── statistics.py # Statistics routes
│   ├── services/        # Business logic
│   ├── utils/           # Helper functions
│   │   ├── response.py  # Response formatters
│   │   └── validators.py # Input validators
│   └── __init__.py      # App factory
├── config/              # Configuration
│   └── config.py       # Config classes
├── tests/              # Unit tests
├── run.py             # Entry point
└── requirements.txt   # Dependencies
```

## API Endpoints

### Health Check
- `GET /health` - Check API health

### Matches
- `GET /api/v1/matches` - Get all matches
- `GET /api/v1/matches/:id` - Get match by ID
- `GET /api/v1/matches/player/:name` - Get player matches
- `GET /api/v1/matches/champion/:name` - Get champion matches

### Players
- `GET /api/v1/players` - Get all players
- `GET /api/v1/players/:puuid` - Get player by PUUID
- `GET /api/v1/players/leaderboard` - Get leaderboard
- `GET /api/v1/players/tier-distribution` - Get tier distribution

### Statistics
- `GET /api/v1/statistics/champions` - Get champion stats
- `GET /api/v1/statistics/player/:name` - Get player stats
- `GET /api/v1/statistics/teams` - Get team stats
- `GET /api/v1/statistics/overview` - Get overview

## Configuration

Edit `config/config.py` for different environments:
- `DevelopmentConfig` - Development settings
- `ProductionConfig` - Production settings
- `TestingConfig` - Testing settings

## Testing

```bash
pytest
```

## MongoDB Schema

### Matches Collection
```javascript
{
  matchId: "NA1_5348438296",
  gameInfo: { ... },
  timestamps: { ... },
  teams: [ ... ],
  participants: [ ... ]
}
```

### Players Collection
```javascript
{
  puuid: "CEAj3J8Z...",
  tier: "PLATINUM",
  rank: "I",
  leaguePoints: 72,
  wins: 106,
  losses: 109
}
```

## Development

### Adding New Endpoints

1. Create route in `app/routes/`
2. Register blueprint in `app/__init__.py`
3. Add model methods if needed
4. Test with Postman or curl

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings
- Add unit tests

## Deployment

### Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Use strong `SECRET_KEY`
- [ ] Configure production MongoDB URI
- [ ] Enable HTTPS
- [ ] Set up logging
- [ ] Configure CORS properly
- [ ] Add rate limiting
- [ ] Set up monitoring

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```
