# 🚀 START HERE - One-Click Setup

## ⚡ Super Quick Start (3 Steps)

### **Step 1: Run Setup (ONE TIME ONLY)**
Double-click: **`setup.bat`**

This will automatically:
- ✅ Check if MongoDB is running
- ✅ Check if data is loaded (asks if you want to load it)
- ✅ Install backend dependencies (Flask, MongoDB, etc.)
- ✅ Install frontend dependencies (Angular, Chart.js, etc.)

**Time:** 15-20 minutes total (mostly data loading)

---

### **Step 2: Start the Application**
Double-click: **`start-all.bat`**

This will:
- Start the backend server (Flask on port 5000)
- Start the frontend server (Angular on port 4200)
- Both open in separate windows

**Time:** 10-15 seconds to start

---

### **Step 3: Open Your Browser**
Go to: **http://localhost:4200**

You should see your beautiful dashboard! 🎮📊

---

## 🛠️ Alternative - Manual Start

If you prefer to start servers separately:

1. **Backend:** Double-click `start-backend.bat`
2. **Frontend:** Double-click `start-frontend.bat`
3. **Browser:** http://localhost:4200

---

## 🔍 Troubleshooting

### Check System Status
Double-click: **`check-status.bat`**

This shows:
- ✓ Python installed?
- ✓ Node.js installed?
- ✓ MongoDB running?
- ✓ Data loaded?
- ✓ Dependencies installed?

---

## 📝 What Each File Does

| File | Purpose |
|------|---------|
| **setup.bat** | One-time setup - installs everything |
| **start-all.bat** | Starts both backend & frontend |
| **start-backend.bat** | Starts only backend (Flask) |
| **start-frontend.bat** | Starts only frontend (Angular) |
| **check-status.bat** | Checks if everything is installed |
| **check_data.py** | Checks if MongoDB has match data |

---

## ⚠️ Common Issues

### "MongoDB is not running"
```cmd
net start MongoDB
```

### "Python not found"
- Make sure Python is installed
- Add Python to your PATH

### "npm not found"
- Make sure Node.js is installed
- Restart your computer after installing Node.js

### Servers won't start
1. Run `check-status.bat` to see what's missing
2. Make sure ports 5000 and 4200 are not in use
3. Close other programs using these ports

---

## 🎯 Quick Reference

**Backend API:** http://localhost:5000
- Health check: http://localhost:5000/health
- API docs: http://localhost:5000/api/v1

**Frontend App:** http://localhost:4200
- Dashboard: http://localhost:4200/dashboard
- Matches: http://localhost:4200/matches
- Players: http://localhost:4200/players
- Statistics: http://localhost:4200/statistics

---

## 🎮 Features You'll See

### Dashboard Page
- Total matches count
- Average game duration
- Top champion with win rate
- Team side win rates (Blue vs Red)
- Top 15 champions performance charts
- Recent matches preview

### Matches Page
- Browse all 101,843 matches
- Pagination for easy navigation
- Click any match for detailed view

### Match Detail Page
- Full participant lists for both teams
- KDA statistics with color coding
- Team objectives (dragons, baron, towers)
- Gold and damage comparisons

### Players Page
- Grid of all players with tier badges
- Color-coded rank badges

### Statistics Page
- Interactive charts for champion stats
- Win rates, pick rates, average KDA
- Comprehensive data table
- Sortable columns

---

## 🔥 Ready to Start?

1. Double-click **`setup.bat`** (first time only)
2. Double-click **`start-all.bat`**
3. Open browser to **http://localhost:4200**

**Enjoy your League of Legends Analytics Platform!** 🏆

---

## 💡 Tips

- Keep the terminal windows open while using the app
- Press `Ctrl+C` in the terminals to stop the servers
- The frontend auto-reloads when you make changes
- The backend also auto-reloads in development mode

---

## 🆘 Need Help?

If something doesn't work:
1. Run `check-status.bat` to diagnose
2. Check the terminal windows for error messages
3. Make sure MongoDB is running: `net start MongoDB`
4. Restart the servers by closing terminals and running `start-all.bat` again

**You've got this!** 🚀
