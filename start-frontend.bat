@echo off
echo ================================================================
echo   Starting Angular Frontend Server
echo ================================================================
echo.

cd frontend

echo Starting Angular development server...
echo Server will be available at http://localhost:4200
echo Press Ctrl+C to stop the server
echo ================================================================
echo.

call npm start

pause
