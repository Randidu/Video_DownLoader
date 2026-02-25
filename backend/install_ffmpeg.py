import os
import zipfile
import shutil
import urllib.request
import sys
from pathlib import Path

def install_ffmpeg():
    print("Starting FFmpeg installation...")
    
    # URL for a lightweight static build of FFmpeg (essentials)
    # Using gyan.dev which is the standard source for Windows git builds
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = "ffmpeg.zip"
    extract_dir = "ffmpeg_temp"
    
    # 1. Download
    print(f"Downloading FFmpeg from {url}...")
    try:
        urllib.request.urlretrieve(url, zip_path)
        print("Download complete.")
    except Exception as e:
        print(f"Failed to download: {e}")
        return False

    # 2. Extract
    print("Extracting...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
    except Exception as e:
        print(f"Failed to extract: {e}")
        return False

    # 3. Locate and Move bin files
    print("Locating binaries...")
    bin_files = ['ffmpeg.exe', 'ffprobe.exe']
    found = 0
    
    # Search recursively for the bin folder or the files directly
    for root, dirs, files in os.walk(extract_dir):
        for file in files:
            if file in bin_files:
                src = os.path.join(root, file)
                dst = os.path.join(os.getcwd(), file)
                print(f"Moving {file} to project root...")
                try:
                    shutil.move(src, dst)
                    found += 1
                except Exception as e:
                    print(f"Error moving {file}: {e}")
                    # If file exists, try to replace it? or just pass
                    # On windows, can't replace executed file. 
                    pass

    # 4. Cleanup
    print("Cleaning up...")
    try:
        os.remove(zip_path)
        shutil.rmtree(extract_dir)
    except Exception as e:
        print(f"Cleanup warning: {e}")

    if found >= 2:
        print("Successfully installed FFmpeg and FFprobe!")
        return True
    else:
        print(f"Something went wrong. Found {found}/2 binaries.")
        return False

if __name__ == "__main__":
    install_ffmpeg()
