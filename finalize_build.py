import shutil
import os
import time

dist = "dist/Video Downloader"

print(f"Waiting for {dist} to be created by PyInstaller...")
# Wait up to 5 minutes
for i in range(60):
    if os.path.exists(dist):
        break
    time.sleep(5)

if not os.path.exists(dist):
    print("Timed out waiting for build directory.")
    exit(1)

# Wait a bit more for PyInstaller to finish writing exe? 
# Actually PyInstaller writes into dist at the end.
# But we can just copy safely.

print("Copying assets to distribution folder...")
try:
    shutil.copy("index.html", dist)
    print("- Copied index.html")
    
    if os.path.exists("ffmpeg.exe"):
        shutil.copy("ffmpeg.exe", dist)
        print("- Copied ffmpeg.exe")
        
    if os.path.exists("ffprobe.exe"):
        shutil.copy("ffprobe.exe", dist)
        print("- Copied ffprobe.exe")
        
    print(f"\nSUCCESS! Your standalone app is ready at: {os.path.abspath(dist)}")
    print("You can zip this folder and share it.")
except Exception as e:
    print(f"Error copying files: {e}")
