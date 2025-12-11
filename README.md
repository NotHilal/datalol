# League of Legends Match Analytics Platform

A full-stack web application for analyzing League of Legends match data, featuring a Flask backend API and Angular frontend dashboard.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Features](#features)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)

## 🎯 Project Overview

This platform provides comprehensive analytics for League of Legends matches, including:
- Match history and detailed match analysis
- Player statistics and performance metrics
- Champion win rates and statistics
- Team composition analysis
- Interactive data visualizations

## 🛠 Tech Stack

### Backend
- **Flask** - Python web framework
- **MongoDB** - NoSQL database for match data
- **Pymongo** - MongoDB driver for Python
- **Flask-CORS** - Cross-origin resource sharing

### Frontend
- **Angular 17** - Frontend framework
- **TypeScript** - Type-safe JavaScript
- **RxJS** - Reactive programming
- **Chart.js** - Data visualization
- **SCSS** - Styling

## 📁 Project Structure

```
league-of-legends-project/
├── backend/                    # Flask backend
│   ├── app/
│   │   ├── models/            # MongoDB models
│   │   ├── routes/            # API endpoints
│   │   ├── services/          # Business logic
│   │   ├── utils/             # Helper functions
│   │   ├── middlewares/       # Custom middlewares
│   │   └── __init__.py        # App factory
│   ├── config/                # Configuration files
│   ├── tests/                 # Unit tests
│   ├── migrations/            # Database migrations
│   ├── static/                # Static files
│   ├── run.py                 # Application entry point
│   ├── requirements.txt       # Python dependencies
│   └── .env.example           # Environment variables template
│
├── frontend/                  # Angular frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/   # Reusable components
│   │   │   ├── pages/        # Page components
│   │   │   ├── services/     # API services
│   │   │   ├── models/       # TypeScript interfaces
│   │   │   ├── shared/       # Shared modules
│   │   │   ├── app.module.ts
│   │   │   └── app-routing.module.ts
│   │   ├── assets/           # Static assets
│   │   ├── environments/     # Environment configs
│   │   └── styles.scss       # Global styles
│   ├── angular.json          # Angular configuration
│   ├── package.json          # Node dependencies
│   └── tsconfig.json         # TypeScript configuration
│
├── data/                      # Data files
│   ├── matchData.csv
│   ├── match_data.jsonl
│   ├── match_ids.csv
│   └── players_8-14-25.csv
│
├── scripts/                   # Utility scripts
│   └── load_to_mongodb.py    # Data loading script
│
├── docker/                    # Docker configurations (future)
├── .gitignore
└── README.md
```

## ✅ Prerequisites

- **Python 3.8+**
- **Node.js 18+** and npm
- **MongoDB 5.0+**
- **Angular CLI**: `npm install -g @angular/cli`

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/NotHilal/datalol.git
cd datalol
```

**Important Note:** The large data files (`matchData.csv` and `match_data.jsonl`) are not included in the repository due to GitHub's file size limits. You'll need to either:
- Copy these files from your original project to the `data/` folder, or
- Generate new data using the Riot API, or
- Request the data files separately from the project maintainer

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your configuration
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install
```

### 4. Database Setup

```bash
# Start MongoDB (if not already running)
mongod

# Load data into MongoDB
cd ..
python scripts/load_to_mongodb.py
```

## 🚀 Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python run.py
```

Backend will run on `http://localhost:5000`

### Start Frontend (Terminal 2)

```bash
cd frontend
npm start
```

Frontend will run on `http://localhost:4200`

### Access the Application

Open your browser and navigate to `http://localhost:4200`

## 🎨 Features

### Match Analytics
- View match history with pagination
- Detailed match breakdown
- Team composition analysis
- Objective timeline

### Player Statistics
- Player profile and performance metrics
- Match history per player
- KDA statistics
- Win rate analysis

### Champion Statistics
- Champion win rates
- Average performance metrics
- Pick/ban rates
- Role distribution

### Data Visualizations
- Win rate charts
- Performance trends
- Team statistics
- Distribution graphs

## 📚 API Documentation

### Base URL
```
http://localhost:5000/api/v1
```

### Endpoints

#### Matches
- `GET /matches` - Get all matches (paginated)
- `GET /matches/:id` - Get match by ID
- `GET /matches/player/:name` - Get matches by player
- `GET /matches/champion/:name` - Get matches by champion

#### Players
- `GET /players` - Get all players (paginated)
- `GET /players/:puuid` - Get player by PUUID
- `GET /players/leaderboard` - Get top players
- `GET /players/tier-distribution` - Get tier distribution

#### Statistics
- `GET /statistics/champions` - Get champion statistics
- `GET /statistics/player/:name` - Get player statistics
- `GET /statistics/teams` - Get team statistics
- `GET /statistics/overview` - Get overview statistics

For detailed API documentation, see [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🔧 Development

### Backend Development
- Follow PEP 8 style guide
- Write unit tests for new features
- Use type hints where applicable
- Document API endpoints

### Frontend Development
- Follow Angular style guide
- Use TypeScript strict mode
- Create reusable components
- Implement responsive design

## 📝 Environment Variables

### Backend (.env)
```
FLASK_ENV=development
MONGO_URI=mongodb://localhost:27017/
MONGO_DB_NAME=lol_matches
SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:4200
```

### Frontend (environment.ts)
```typescript
export const environment = {
  production: false,
  apiUrl: 'http://localhost:5000/api/v1'
};
```

## 🐳 Docker Deployment (Optional)

```bash
# Build and run with Docker Compose (future)
docker-compose up --build
```

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📧 Contact

For questions or support, please open an issue in the repository.

---

Built with ❤️ for League of Legends analytics
