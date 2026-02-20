@echo off
echo ==========================================
echo    Building Portable Video Downloader
echo ==========================================

echo [step 1/2] Cleaning previous builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

echo [step 2/2] Running PyInstaller...
pyinstaller "Video Downloader.spec" --clean --noconfirm

if %errorlevel% neq 0 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo [step 3/3] Copying assets...
copy "index.html" "dist\Video Downloader\"
if exist "ffmpeg.exe" copy "ffmpeg.exe" "dist\Video Downloader\"
if exist "ffprobe.exe" copy "ffprobe.exe" "dist\Video Downloader\"

echo.
echo ==========================================
echo          BUILD SUCCESSFUL
echo ==========================================
echo.
echo Your portable app is located in: dist\Video Downloader
echo.
pause
