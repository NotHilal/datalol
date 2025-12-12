@echo off
echo ================================================================
echo   System Status Check
echo ================================================================
echo.

echo Checking Python...
py --version 2>nul || python --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python not found in PATH
) else (
    echo ✓ Python is installed
)

echo.
echo Checking Node.js...
node --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js not found in PATH
) else (
    echo ✓ Node.js is installed
)

echo.
echo Checking npm...
call npm --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ npm not found in PATH
) else (
    echo ✓ npm is installed
)

echo.
echo Checking MongoDB...
sc query MongoDB | find "RUNNING" >nul
if %errorlevel% neq 0 (
    echo ❌ MongoDB is not running
    echo    Run: net start MongoDB
) else (
    echo ✓ MongoDB is running
)

echo.
echo Checking MongoDB data...
if exist check_data.py (
    py check_data.py 2>nul || python check_data.py
) else (
    echo ⚠ check_data.py not found
)

echo.
echo Checking backend dependencies...
if exist "backend\venv\" (
    echo ✓ Virtual environment exists
) else (
    echo ⚠ No virtual environment found
)

echo.
echo Checking frontend dependencies...
if exist "frontend\node_modules\" (
    echo ✓ Frontend dependencies installed
) else (
    echo ❌ Frontend dependencies not installed
    echo    Run: cd frontend && npm install
)

echo.
echo ================================================================
pause
