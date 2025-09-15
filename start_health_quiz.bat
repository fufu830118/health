@echo off
cd /d "%~dp0"

echo.
echo ============================================================
echo               Health Quiz System Launcher
echo ============================================================
echo.
echo Checking virtual environment...

if not exist "venv\Scripts\python.exe" (
    echo Error: Virtual environment not found
    echo Please run: python -m venv venv
    echo Then run: venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

echo Virtual environment found
echo Starting Health Quiz System...
echo.
echo Server will start at: http://127.0.0.1:5000
echo.

venv\Scripts\python.exe app.py

pause