@echo off
echo ================================================================
echo  PERFORMANCE OPTIMIZATIONS SETUP
echo ================================================================
echo.

echo [1/4] Installing backend dependencies...
cd backend
pip install Flask-Caching==2.1.0 redis==5.0.1
echo   ✓ Dependencies installed
echo.

echo [2/4] Checking Redis connection...
redis-cli ping > nul 2>&1
if %errorlevel% == 0 (
    echo   ✓ Redis is running
) else (
    echo   ⚠ Redis not found - will use simple in-memory cache
    echo   ℹ To install Redis: docker run -d -p 6379:6379 redis
)
echo.

echo [3/4] Building inverted indexes...
echo   This will create optimized lookup tables for players and champions
python scripts/build_inverted_indexes.py
echo.

echo [4/4] Setup complete!
echo.
echo ================================================================
echo  NEXT STEPS:
echo ================================================================
echo  1. Start backend:  python run.py
echo  2. Start frontend: cd ../frontend ^&^& npm start
echo  3. Open browser:   http://localhost:4200
echo  4. Check console for optimization confirmations
echo.
echo  📖 Documentation: See OPTIMIZATIONS.md
echo ================================================================
echo.

pause
