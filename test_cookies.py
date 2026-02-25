
import os
import sys
import logging
from pathlib import Path
import yt_dlp

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

def check_cookies():
    print("=== YouTube Cookie Checker ===")
    
    # 1. Check for cookies.txt
    cookie_file = Path.cwd() / "cookies.txt"
    if cookie_file.exists():
        print(f"[SUCCESS] Found cookies.txt at: {cookie_file}")
        print("Using this file for authentication.")
        return {'cookiefile': str(cookie_file)}
    else:
        print("[INFO] No cookies.txt found in the current directory.")

    # 2. Check for browser cookies
    print("\nChecking for browser cookies...")
    available_browsers = []
    
    # Simple check based on main.py logic
    if os.path.exists(os.path.expandvars(r"%LocalAppData%\Google\Chrome\User Data")):
        available_browsers.append("chrome")
    if os.path.exists(os.path.expandvars(r"%LocalAppData%\Microsoft\Edge\User Data")):
        available_browsers.append("edge")
    if os.path.exists(os.path.expandvars(r"%AppData%\Mozilla\Firefox\Profiles")):
        available_browsers.append("firefox")
    if os.path.exists(os.path.expandvars(r"%LocalAppData%\BraveSoftware\Brave-Browser\User Data")):
        available_browsers.append("brave")
        
    if available_browsers:
        print(f"[SUCCESS] Detected browsers: {', '.join(available_browsers)}")
        print(f"Will attempt to use cookies from: {available_browsers[0]}")
        print("Note: Browser must be CLOSED for this to work reliably.")
        return {'cookiesfrombrowser': (available_browsers[0],)}
    
    print("[WARNING] No supported browsers or cookies.txt found.")
    return {}

def test_download(cookie_kwargs):
    print("\n=== Testing YouTube Connection ===")
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # Rick Roll
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True, # Don't download, just get info
        **cookie_kwargs
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Fetching info for: {url}")
            info = ydl.extract_info(url, download=False)
            print(f"[SUCCESS] Successfully fetched video info: {info.get('title')}")
            print("Cookies are working correctly!")
    except Exception as e:
        print(f"\n[ERROR] Failed to fetch video info: {str(e)}")
        if "Sign in to confirm you’re not a bot" in str(e):
             print("\n!!! BOT DETECTION TRIGGERED !!!")
             print("Please follow the steps in COOKIES_SETUP.md to export cookies.txt")

if __name__ == "__main__":
    cookie_kwargs = check_cookies()
    if cookie_kwargs:
        test_download(cookie_kwargs)
    else:
        print("\nPlease setup cookies.txt or install a supported browser.")
