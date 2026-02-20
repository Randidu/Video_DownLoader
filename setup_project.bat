@echo off
echo ==========================================
echo    Video Downloader Project Setup
echo ==========================================

echo [step 1/3] Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)
echo Python found.

echo [step 2/3] Setting up Virtual Environment...
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

echo [step 3/3] Installing Dependencies...
call venv\Scripts\activate
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo           SETUP SUCCESSFUL
echo ==========================================
echo.
echo You can now run the project using: run_project.bat
echo.
pause
