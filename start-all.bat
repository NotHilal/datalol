@echo off
echo ================================================================
echo   Starting League of Legends Analytics Platform
echo ================================================================
echo.

REM Check MongoDB
echo Checking MongoDB...
sc query MongoDB | find "RUNNING" >nul
if %errorlevel% neq 0 (
    echo Starting MongoDB...
    net start MongoDB
    timeout /t 2 >nul
)
echo ✓ MongoDB is running
echo.

REM Start backend in new window
echo Starting Backend Server...
start "LoL Analytics - Backend" cmd /k "cd /d %~dp0backend && python run.py"
timeout /t 3 >nul

REM Start frontend in new window
echo Starting Frontend Server...
start "LoL Analytics - Frontend" cmd /k "cd /d %~dp0frontend && npm start"

timeout /t 5 >nul
echo.
echo ================================================================
echo ✅ Both servers are starting!
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:4200
echo.
echo Wait about 10-15 seconds for the frontend to compile,
echo then open your browser to: http://localhost:4200
echo.
echo Close the backend and frontend windows to stop the servers.
echo ================================================================
echo.
pause
