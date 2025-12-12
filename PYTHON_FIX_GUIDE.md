# Python Command Not Found - Fix Guide

## The Problem

Windows has "App Execution Aliases" that redirect `python` and `python3` commands to the Microsoft Store. This causes the error:
```
Python was not found; run without arguments to install from the Microsoft Store
```

## Quick Fix (Recommended)

### Method 1: Disable Windows Store Python Alias

1. Press `Windows Key`
2. Type: **Manage app execution aliases**
3. Press `Enter`
4. Scroll down to find **python.exe** and **python3.exe**
5. **Turn OFF** both toggles (disable them)
6. Close the settings window
7. Open a NEW Command Prompt and test:
   ```bash
   python --version
   ```

### Method 2: Use the Full Python Path (Already Implemented)

I've updated all your batch files to automatically find Python using the full path:
```
C:\Users\hilal\AppData\Local\Programs\Python\Python313\python.exe
```

**Your batch files now try in this order:**
1. `py` command (Python launcher)
2. `python` command
3. Full path: `C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python313\python.exe`
4. Alternative path: `C:\Python313\python.exe`

## Updated Files

✅ **start-backend.bat** - Now has robust Python detection
✅ **setup.bat** - Already updated with `py` command
✅ **start-all.bat** - Already updated
✅ **check-status.bat** - Already updated
✅ **test-and-load-data.bat** - Uses `py` or `python` fallback

## What to Do Now

**Option 1: Run fix-python-path.bat**
```bash
fix-python-path.bat
```
This will guide you through disabling the Windows Store aliases.

**Option 2: Just run start-backend.bat again**
```bash
start-backend.bat
```
The updated script should now find Python automatically!

## Testing Python Works

Run this in Command Prompt:
```bash
cmd.exe /c "python test_data_path.py"
```

Or open Command Prompt and type:
```bash
python --version
```

If it still shows the Microsoft Store error, use **Method 1** above.

## Summary

Your project is configured correctly! The issue is just Windows intercepting the `python` command. Once you disable the Windows Store aliases (Method 1), everything will work smoothly.
