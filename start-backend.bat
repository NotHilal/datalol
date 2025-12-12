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

REM Try multiple Python commands
where py >nul 2>&1
if %errorlevel% equ 0 (
    py run.py
    goto end
)

where python >nul 2>&1
if %errorlevel% equ 0 (
    python run.py
    goto end
)

REM Try common Python installation paths
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" (
    "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" run.py
    goto end
)

if exist "C:\Python313\python.exe" (
    C:\Python313\python.exe run.py
    goto end
)

echo ❌ Could not find Python installation
echo Please run fix-python-path.bat to configure Python

:end
pause
