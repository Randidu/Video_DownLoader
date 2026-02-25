@echo off
echo ============================================================
echo   InfinityGrab - Starting Backend API Server
echo   Using Python virtual environment (.venv)
echo ============================================================
cd /d "%~dp0backend"
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: .venv not found! Run setup first.
    pause
    exit /b 1
)
call .venv\Scripts\activate.bat
python main.py
pause
