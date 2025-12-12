@echo off
echo Testing Python installation...
echo.

echo Test 1: Using 'py' command
py --version
if %errorlevel% equ 0 (
    echo ✓ 'py' command works!
    echo.
    echo Test 2: Testing pip with 'py'
    py -m pip --version
    if %errorlevel% equ 0 (
        echo ✓ pip works with 'py' command!
        goto success
    )
)

echo.
echo Test 3: Using 'python' command
python --version
if %errorlevel% equ 0 (
    echo ✓ 'python' command works!
    echo.
    echo Test 4: Testing pip with 'python'
    python -m pip --version
    if %errorlevel% equ 0 (
        echo ✓ pip works with 'python' command!
        goto success
    )
)

echo.
echo ❌ Neither 'py' nor 'python' commands work properly.
echo Please ensure Python is installed and in your PATH.
goto end

:success
echo.
echo ================================================================
echo ✅ Python is configured correctly!
echo You can now run setup.bat
echo ================================================================

:end
echo.
pause
