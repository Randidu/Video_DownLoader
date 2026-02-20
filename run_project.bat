@echo off
echo ==========================================
echo    Starting Video Downloader (Dev Mode)
echo ==========================================

if not exist venv (
    echo [ERROR] Virtual environment not found!
    echo Please run 'setup_project.bat' first.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Starting server...
echo The application will open in your default browser.
python main.py

pause
