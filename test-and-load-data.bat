@echo off
echo ================================================================
echo   Data Loading Test and Execution
echo ================================================================
echo.

echo Step 1: Testing if data file exists...
echo.
py test_data_path.py 2>nul || python test_data_path.py
echo.

echo ================================================================
echo.
echo Step 2: Checking MongoDB connection and current data...
echo.
py check_data.py 2>nul || python check_data.py
echo.

echo ================================================================
echo.
set /p CONTINUE="Do you want to load the data now? (Y/N): "
if /i "%CONTINUE%" neq "Y" goto end

echo.
echo Step 3: Loading data into MongoDB...
echo This will take 10-15 minutes. Please wait...
echo.
py scripts\load_to_mongodb.py 2>nul || python scripts\load_to_mongodb.py

if %errorlevel% equ 0 (
    echo.
    echo ✅ Data loading completed!
    echo.
    echo Step 4: Verifying data...
    py check_data.py 2>nul || python check_data.py
) else (
    echo.
    echo ❌ Data loading failed. Please check the error messages above.
)

:end
echo.
echo ================================================================
pause
