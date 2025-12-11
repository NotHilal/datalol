# Quick Start Guide - League of Legends Analytics

## 🚀 Setup on a New PC

### Step 0: Clone the Repository

```bash
git clone https://github.com/NotHilal/datalol.git
cd datalol
```

**⚠️ IMPORTANT:** The large data files are NOT included in the repository. You need to:
1. Copy `matchData.csv` and `match_data.jsonl` from your original project into the `data/` folder
2. Or skip to Step 2 and the data loader will fail - you'll need the original data files

## Prerequisites Check
- Python 3.8+ installed
- Node.js 18+ installed
- MongoDB needs to be installed and running
- Backend dependencies need to be installed
- Frontend dependencies need to be installed

---

## Step 1: Install and Start MongoDB

### Windows:
```bash
# Download from: https://www.mongodb.com/try/download/community
# Install with default settings
# Start MongoDB service
net start MongoDB
```

### Docker (Alternative):
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### Verify MongoDB is running:
```bash
mongosh --eval "db.version()"
```

---

## Step 2: Load Data into MongoDB

**⚠️ Make sure you have copied the data files to the `data/` folder first!**

```bash
# From the project root directory (datalol)
python scripts/load_to_mongodb.py

# On Windows use:
python scripts\load_to_mongodb.py
```

**This will take 10-15 minutes to load 101,843 matches!**

---

## Step 3: Setup and Start Backend

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the Flask backend
python run.py
```

**Backend will run on: http://localhost:5000**

Test it by opening: http://localhost:5000/health

---

## Step 4: Setup and Start Frontend

Open a **NEW terminal** window:

```bash
# Navigate to frontend folder
cd C:\Users\hilal\Downloads\archive(1)\league-of-legends-project\frontend

# Install dependencies (takes 2-3 minutes)
npm install

# Start the Angular development server
npm start
```

**Frontend will run on: http://localhost:4200**

---

## Step 5: Access the Application

Open your browser and go to: **http://localhost:4200**

You should see:
- 🏠 **Dashboard** - Overview with statistics and charts
- 🎮 **Matches** - Browse all matches with pagination
- 👥 **Players** - View all players
- 📊 **Statistics** - Detailed champion analytics

---

## Features Implemented

### Frontend Components ✅
- ✅ Match Cards - Display match info with team stats
- ✅ Player Stats Cards - Show player performance metrics
- ✅ Interactive Charts - Win rates, KDA, champion stats using Chart.js
- ✅ Pagination - Navigate through large datasets
- ✅ Responsive Navbar - Easy navigation

### Pages ✅
- ✅ Dashboard - Overview with stats and recent matches
- ✅ Matches List - Browse all matches
- ✅ Match Detail - Detailed view of individual match
- ✅ Players List - All registered players
- ✅ Player Detail - Individual player statistics
- ✅ Statistics - Comprehensive champion analytics

### Backend API ✅
- ✅ Match endpoints (list, detail, by player, by champion)
- ✅ Player endpoints (list, detail, leaderboard, tier distribution)
- ✅ Statistics endpoints (champions, players, teams, overview)
- ✅ MongoDB integration with indexes for performance
- ✅ Pagination support
- ✅ CORS configured for frontend

---

## Troubleshooting

### MongoDB Connection Error
```bash
# Check if MongoDB is running
net start MongoDB

# Or restart it
net stop MongoDB
net start MongoDB
```

### Backend Import Errors
```bash
# Make sure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Errors
```bash
# Delete node_modules and reinstall
rm -rf node_modules
npm install
```

### Port Already in Use
```bash
# Backend: Change FLASK_PORT in .env file
# Frontend: Use different port
npm start -- --port 4300
```

---

## What's Next?

### Currently Working: Frontend UI ✅ COMPLETE
- ✅ All components created
- ✅ All pages implemented
- ✅ Routing configured
- ✅ Charts integrated

### Still Pending (Optional):
1. **Machine Learning Features** - Match prediction, player clustering
2. **Testing** - Unit tests for backend and frontend
3. **Deployment** - Docker configuration, cloud deployment
4. **Advanced Features** - Redis caching, feature engineering

---

## Quick Commands Reference

### Start Everything (3 separate terminals)

**Terminal 1 - MongoDB:**
```bash
net start MongoDB
```

**Terminal 2 - Backend:**
```bash
cd backend
venv\Scripts\activate
python run.py
```

**Terminal 3 - Frontend:**
```bash
cd frontend
npm start
```

---

## Need Help?

Check the documentation:
- `README.md` - Full project documentation
- `API_DOCUMENTATION.md` - API reference
- `PROJECT_STRUCTURE.md` - Architecture details
- `SETUP_GUIDE.md` - Detailed setup instructions

---

**Enjoy your League of Legends Analytics Platform!** 🎮📊
