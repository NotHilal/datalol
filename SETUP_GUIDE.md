# Quick Setup Guide

## Prerequisites Checklist
- [x] Python 3.13.9 installed ✅
- [x] Node.js v22.16.0 installed ✅
- [x] Project structure created ✅
- [x] Data files copied ✅
- [ ] MongoDB installed ⚠️
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Data loaded into MongoDB
- [ ] Backend running
- [ ] Frontend running

---

## Setup Steps

### 1. Install MongoDB

**Windows (Recommended):**
1. Download: https://www.mongodb.com/try/download/community
2. Install with default settings
3. Start service: `net start MongoDB`

**Docker (Alternative):**
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

**Verify MongoDB is running:**
```bash
mongosh --eval "db.version()"
```

---

### 2. Setup Backend

```bash
# Navigate to backend folder
cd C:\Users\hilal\Downloads\archive(1)\league-of-legends-project\backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**✅ .env file already created!**

---

### 3. Setup Frontend

```bash
# Open NEW terminal
cd C:\Users\hilal\Downloads\archive(1)\league-of-legends-project\frontend

# Install dependencies (will take 2-3 minutes)
npm install
```

---

### 4. Load Data into MongoDB

```bash
# Make sure MongoDB is running first!
# Navigate to scripts folder
cd C:\Users\hilal\Downloads\archive(1)\league-of-legends-project

# Copy the loader script
cp ..\load_to_mongodb.py scripts\

# Update the script path
```

Then edit `scripts\load_to_mongodb.py` line 18:
```python
CSV_FILE_PATH = r"C:\Users\hilal\Downloads\archive(1)\league-of-legends-project\data\matchData.csv"
```

Run the loader:
```bash
python scripts\load_to_mongodb.py
```

**This will take 10-15 minutes to load 101,843 matches!**

---

### 5. Start Backend Server

```bash
# Terminal 1 - Backend
cd C:\Users\hilal\Downloads\archive(1)\league-of-legends-project\backend
venv\Scripts\activate
python run.py
```

**Backend will run on: http://localhost:5000**

Test it:
```bash
# Open browser or use curl:
curl http://localhost:5000/health
```

---

### 6. Start Frontend Server

```bash
# Terminal 2 - Frontend
cd C:\Users\hilal\Downloads\archive(1)\league-of-legends-project\frontend
npm start
```

**Frontend will run on: http://localhost:4200**

---

## Quick Commands Reference

### Backend
```bash
cd backend
venv\Scripts\activate
python run.py
```

### Frontend
```bash
cd frontend
npm start
```

### Load Data
```bash
python scripts\load_to_mongodb.py
```

### MongoDB
```bash
# Start MongoDB
net start MongoDB

# Stop MongoDB
net stop MongoDB

# Connect to MongoDB shell
mongosh
```

---

## Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB service is running: `net start MongoDB`
- Check MongoDB is on port 27017: `mongosh`

### Backend Import Errors
- Activate virtual environment: `venv\Scripts\activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend Errors
- Delete node_modules: `rm -rf node_modules`
- Reinstall: `npm install`

### CORS Errors
- Check backend .env has: `CORS_ORIGINS=http://localhost:4200`
- Restart backend after changes

### Port Already in Use
- Backend: Change FLASK_PORT in .env
- Frontend: Use `npm start -- --port 4300`

---

## What's Next?

After setup is complete:

1. **Test API**: http://localhost:5000/api/v1/matches
2. **View Frontend**: http://localhost:4200
3. **Create Components**: Dashboard, Match List, Player Stats
4. **Add Visualizations**: Charts using Chart.js
5. **Implement Search & Filters**

---

## Project Structure Quick Reference

```
league-of-legends-project/
├── backend/          # Flask API (Port 5000)
│   ├── app/         # Application code
│   ├── config/      # Configuration
│   ├── run.py       # Start here
│   └── .env         # Environment vars ✅
├── frontend/        # Angular App (Port 4200)
│   ├── src/app/     # Angular code
│   ├── package.json # Dependencies
│   └── angular.json # Config
├── data/           # CSV/JSONL files
└── scripts/        # Utility scripts
```

---

## Time Estimates

- MongoDB Installation: 5 minutes
- Backend Setup: 3 minutes
- Frontend Setup: 5 minutes
- Data Loading: 10-15 minutes
- **Total: ~25 minutes**

---

## Need Help?

- Check README.md for detailed documentation
- Check API_DOCUMENTATION.md for API reference
- Check PROJECT_STRUCTURE.md for architecture details
