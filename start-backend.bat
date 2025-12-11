@echo off
echo ================================================================
echo   Starting Flask Backend Server
echo ================================================================
echo.

cd backend

echo Checking MongoDB...
sc query MongoDB | find "RUNNING" >nul
if %errorlevel% neq 0 (
    echo Starting MongoDB...
    net start MongoDB
    timeout /t 2 >nul
)

echo Starting Flask server on http://localhost:5000
echo Press Ctrl+C to stop the server
echo ================================================================
echo.

python run.py

pause
