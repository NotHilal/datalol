@echo off
echo ================================================================
echo   Quick Start - League of Legends Analytics
echo ================================================================
echo.
echo Finding Python installation...
echo.

REM Find Python
set PYTHON_EXE=
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" (
    set PYTHON_EXE=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe
    echo Found Python at: %PYTHON_EXE%
    goto start
)

where py >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_EXE=py
    echo Found Python launcher: py
    goto start
)

where python >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_EXE=python
    echo Found Python: python
    goto start
)

echo ❌ Could not find Python!
echo.
echo Please either:
echo 1. Run fix-python-path.bat to fix Windows Python aliases
echo 2. Install Python from python.org
echo.
pause
exit /b 1

:start
echo.
echo Testing Python...
"%PYTHON_EXE%" --version
if %errorlevel% neq 0 (
    echo ❌ Python test failed
    pause
    exit /b 1
)
echo ✓ Python is working!
echo.

echo ================================================================
echo.
echo [1/3] Checking MongoDB...
sc query MongoDB | find "RUNNING" >nul
if %errorlevel% neq 0 (
    echo Starting MongoDB...
    net start MongoDB
    timeout /t 2 >nul
)
echo ✓ MongoDB is running
echo.

echo [2/3] Starting Backend Server...
start "LoL Analytics - Backend" cmd /k "cd /d %~dp0backend && "%PYTHON_EXE%" run.py"
timeout /t 3 >nul
echo ✓ Backend started
echo.

echo [3/3] Starting Frontend Server...
start "LoL Analytics - Frontend" cmd /k "cd /d %~dp0frontend && npm start"
echo ✓ Frontend starting
echo.

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
