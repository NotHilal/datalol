@echo off
echo ================================================================
echo   League of Legends Analytics - Complete Setup
echo ================================================================
echo.

REM Check if MongoDB is running
echo [1/6] Checking MongoDB...
sc query MongoDB | find "RUNNING" >nul
if %errorlevel% neq 0 (
    echo MongoDB is not running. Starting MongoDB...
    net start MongoDB
    timeout /t 3 >nul
)
echo ✓ MongoDB is running

REM Install backend dependencies FIRST (needed for data loading)
echo.
echo [2/6] Installing backend dependencies...
cd backend
py -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Error installing backend dependencies.
    echo Trying alternative Python command...
    python -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Error installing backend dependencies.
        echo Make sure Python and pip are installed and in your PATH.
        pause
        exit /b 1
    )
)
echo ✓ Backend dependencies installed (including tqdm, pandas, pymongo)
cd ..

REM Check if data is loaded
echo.
echo [3/6] Checking if data is loaded...
py check_data.py 2>nul || python check_data.py
if %errorlevel% neq 0 (
    echo.
    echo Would you like to load the match data now? (This takes 10-15 minutes)
    echo Press Y to load data, or N to skip
    choice /C YN /M "Load data"
    if errorlevel 2 goto skipdata
    if errorlevel 1 goto loaddata
)
goto afterdata

:loaddata
echo.
echo Loading match data into MongoDB...
echo This will take 10-15 minutes. Please wait...
py scripts\load_to_mongodb.py 2>nul || python scripts\load_to_mongodb.py
if %errorlevel% neq 0 (
    echo ❌ Error loading data. Please check the error messages above.
    pause
    exit /b 1
)
echo ✓ Data loaded successfully!
goto afterdata

:skipdata
echo Skipping data load.

:afterdata
echo.
echo [4/6] Installing frontend dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ❌ Error installing frontend dependencies.
    pause
    exit /b 1
)
echo ✓ Frontend dependencies installed
cd ..

echo.
echo [5/6] Verifying setup...
py check_data.py 2>nul || python check_data.py

echo.
echo [6/6] Setup complete!
echo ================================================================
echo.
echo ✅ Everything is ready to run!
echo.
echo To start the application:
echo   Option 1: Run start-all.bat (starts both servers)
echo   Option 2: Run start-backend.bat, then start-frontend.bat
echo.
echo Then open your browser to: http://localhost:4200
echo.
echo ================================================================
pause
