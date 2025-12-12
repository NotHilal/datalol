@echo off
REM Helper script to find and set Python path
REM This is called by other batch files

REM Try py launcher first
where py >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    exit /b 0
)

REM Try python command
where python >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    exit /b 0
)

REM Try common installation path
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe" (
    set PYTHON_CMD=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe
    exit /b 0
)

REM Try another common path
if exist "C:\Python313\python.exe" (
    set PYTHON_CMD=C:\Python313\python.exe
    exit /b 0
)

REM Python not found
set PYTHON_CMD=
exit /b 1
