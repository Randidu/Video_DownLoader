@echo off
echo ============================================================
echo   InfinityGrab - Build Frontend ^& Start Full App
echo   Backend: http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo ============================================================
echo.
echo [1/2] Building frontend into backend/static ...
cd /d "%~dp0frontend"
call npm run build
if %errorlevel% neq 0 (
    echo ERROR: Frontend build failed!
    pause
    exit /b 1
)
echo.
echo [2/2] Starting backend server (with .venv) ...
cd /d "%~dp0backend"
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: .venv not found! Please run:
    echo   cd backend
    echo   py -3.13 -m venv .venv
    echo   .venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)
call .venv\Scripts\activate.bat
python main.py
pause
