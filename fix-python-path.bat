@echo off
echo ================================================================
echo   Python Path Fix - Disabling Windows Store Python Alias
echo ================================================================
echo.

echo The error "Python was not found; run without arguments to install"
echo happens because Windows has a Microsoft Store shortcut that
echo intercepts the 'python' command.
echo.
echo This script will guide you to disable it.
echo.
echo ================================================================
echo MANUAL FIX REQUIRED:
echo ================================================================
echo.
echo Please follow these steps:
echo.
echo 1. Press Windows Key
echo 2. Type: "Manage app execution aliases"
echo 3. Press Enter
echo 4. Scroll down to find "python.exe" and "python3.exe"
echo 5. Turn OFF both toggles (disable them)
echo 6. Close the settings window
echo.
echo After doing this, close this window and run start-backend.bat again
echo.
echo ================================================================
echo.
echo Alternatively, we can use the full Python path directly.
echo Press any key to open the settings page automatically...
pause >nul

start ms-settings:appsfeatures-app

echo.
echo After disabling the aliases, test Python:
echo.
pause
python --version
echo.
pause
