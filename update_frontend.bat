@echo off
echo Copying frontend build to root...
copy /Y "frontend\dist\index.html" . 
copy /Y "frontend\dist\robots.txt" .
copy /Y "frontend\dist\sitemap.xml" .
copy /Y "frontend\dist\logo.png" .
copy /Y "frontend\dist\favicon.ico" .
copy /Y "frontend\dist\manifest.json" .
if exist frontend\dist\assets (
    if not exist assets mkdir assets
    xcopy /Y /S /E "frontend\dist\assets\*" "assets\"
)
echo Frontend updated.
pause
