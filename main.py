from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, HttpUrl
import yt_dlp
from pytubefix import YouTube
from pytubefix.cli import on_progress
import os
import uuid
from pathlib import Path
from typing import Optional, List
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
import shutil
import subprocess

import sys
import tempfile
from urllib.parse import quote

# Configure logging to file and console
log_file_path = Path.cwd() / "server.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file_path, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logging.getLogger("multipart").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Determine the application base path (works for Python script and PyInstaller exe)
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent.resolve()

logger.info(f"Application Base Directory: {BASE_DIR}")

app = FastAPI(title="YouTube & Social Video Downloader API", version="2.1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment Detection (Server vs Desktop)
IS_SERVER = os.environ.get("RENDER") or os.environ.get("DYNO") or os.environ.get("SERVER_ENV")

if IS_SERVER:
    DOWNLOADS_DIR = Path(tempfile.gettempdir()) / "avy_downloads"
    logger.info(f"Running in SERVER mode. Downloads dir: {DOWNLOADS_DIR}")
else:
    DOWNLOADS_DIR = Path.home() / "Downloads"
    logger.info(f"Running in DESKTOP mode. Downloads dir: {DOWNLOADS_DIR}")

DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Mount Static Files
from fastapi.staticfiles import StaticFiles
assets_path = BASE_DIR / "assets"
assets_path.mkdir(exist_ok=True)
app.mount("/assets", StaticFiles(directory=assets_path), name="assets")

# Thread pool
executor = ThreadPoolExecutor(max_workers=4)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled server error: {exc}", exc_info=True)
    return FileResponse(BASE_DIR / "index.html", status_code=500) # Or JSON? 
    # Better to return JSON for API calls, but maybe text for debugging.
    # Let's return a JSON error that the frontend might (or might not) handle, 
    # but primarily we want to ENSURE IT IS LOGGED.
    # Actually, let's keep it simple: generic 500 response, but LOG IT.
    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error", "detail": str(exc)},
    )

class VideoURL(BaseModel):
    url: HttpUrl

class DownloadRequest(BaseModel):
    url: HttpUrl
    format: str = "best"
    quality: Optional[str] = None

def is_youtube_url(url: str) -> bool:
    u = str(url).lower()
    return "youtube.com" in u or "youtu.be" in u

def get_cookie_kwargs():
    """Returns yt-dlp options for cookies (file or browser)."""
    opts = {}

    # 1. Try local cookies.txt first (Best for servers/persistent auth)
    cookie_file = BASE_DIR / "cookies.txt"
    if cookie_file.exists():
        logger.info(f"Using cookie file: {cookie_file}")
        opts['cookiefile'] = str(cookie_file)
    else:
        # 2. Try browser cookies (Best for local dev)
        browser = get_browser_cookies()
        if browser:
            logger.info(f"Using cookies from browser: {browser}")
            opts['cookiesfrombrowser'] = (browser,)

    # Always use tv/mweb player clients — these bypass bot detection and support cookies
    opts['extractor_args'] = {'youtube': {'player_client': ['tv', 'mweb']}}

    return opts

def get_browser_cookies():
    """Returns the name of a browser that is likely to have cookies."""
    # List of common browsers to try in order
    found_browsers = []
    # Chrome
    if os.path.exists(os.path.expandvars(r"%LocalAppData%\Google\Chrome\User Data")):
        found_browsers.append("chrome")
    # Edge
    if os.path.exists(os.path.expandvars(r"%LocalAppData%\Microsoft\Edge\User Data")):
        found_browsers.append("edge")
    # Firefox
    if os.path.exists(os.path.expandvars(r"%AppData%\Mozilla\Firefox\Profiles")):
        found_browsers.append("firefox")
    # Brave
    if os.path.exists(os.path.expandvars(r"%LocalAppData%\BraveSoftware\Brave-Browser\User Data")):
        found_browsers.append("brave")

    if found_browsers:
        # logger.info(f"Detected browsers for cookies: {found_browsers}")
        return found_browsers[0] # Return the first one found
    
    return "chrome" # Default to chrome if nothing detected

def get_best_browser_for_cmd():
    return get_browser_cookies()

def get_deno_path():
    """Find the deno executable path."""
    # Common install locations on Windows
    deno_local = Path.home() / ".deno" / "bin" / "deno.exe"
    if deno_local.exists():
        return str(deno_local)
    if shutil.which("deno"):
        return shutil.which("deno")
    return None

@app.get("/")
async def root():
    html_path = BASE_DIR / "index.html"
    if not html_path.exists():
        logger.error(f"index.html not found at {html_path}")
        return {"error": "index.html not found. Please ensure it exists in the application directory."}
    return FileResponse(html_path)

@app.get("/logo.png")
async def get_logo():
    path = BASE_DIR / "logo.png"
    if path.exists():
        return FileResponse(path)
    return FileResponse(BASE_DIR / "assets" / "logo.png") # Fallback

@app.get("/favicon.ico")
async def get_favicon():
    path = BASE_DIR / "favicon.ico"
    if path.exists():
        return FileResponse(path)
    # Check if logo.png exists and serve it as fallback? 
    # Or just return logo.png as favicon.ico content type?
    # Better to just return logo.png if favicon.ico missing.
    return await get_logo()

@app.get("/manifest.json")
async def get_manifest():
    return FileResponse(BASE_DIR / "manifest.json")

@app.get("/robots.txt")
async def get_robots():
    return FileResponse(BASE_DIR / "robots.txt")

@app.get("/sitemap.xml")
async def get_sitemap():
    return FileResponse(BASE_DIR / "sitemap.xml")

@app.post("/video/info")
async def get_video_info(video: VideoURL):
    url_str = str(video.url)
    
    # helper for yt-dlp info
    def get_info_ytdlp():
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            **get_cookie_kwargs(),
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'socket_timeout': 30,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url_str, download=False)

    try:
        # Use yt-dlp for everything (more robust against bot detection for info fetching)
        info = await asyncio.get_event_loop().run_in_executor(executor, get_info_ytdlp)
        return {
            "success": True,
            "data": {
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration'),
                "uploader": info.get('uploader'),
                "view_count": info.get('view_count'),
            }
        }
            
    except Exception as e:
        logger.error(f"Error info: {e}")
        raise HTTPException(status_code=400, detail=str(e))

def cleanup_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
            logger.info(f"Cleaned up file: {path}")
    except Exception as e:
        logger.warning(f"Failed to cleanup file {path}: {e}")

from fastapi.responses import StreamingResponse

@app.get("/video/download_link")
async def download_link_get(url: str, background_tasks: BackgroundTasks, format: str = "best", quality: str = None):
    url_str = url
    
    # Check for FFmpeg
    ffmpeg_exe = "ffmpeg"
    local_ffmpeg = BASE_DIR / "ffmpeg.exe"
    if local_ffmpeg.exists():
        ffmpeg_exe = str(local_ffmpeg)
    elif shutil.which("ffmpeg"):
         ffmpeg_exe = "ffmpeg"
    else:
         ffmpeg_exe = None

    try:

        # 1. Get Metadata (Title/Filename/Size) quickly
        def get_meta():
            ydl_opts = {
                'quiet': True, 
                'no_warnings': True,
                **get_cookie_kwargs(),
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url_str, download=False)
                filename = ydl.prepare_filename(info)
                # Try to get filesize
                size = info.get('filesize') or info.get('filesize_approx')
                return filename, size
        
        filesize = None
        try:
            suggested_filename, filesize = await asyncio.get_event_loop().run_in_executor(executor, get_meta)
            filename = os.path.basename(suggested_filename)
        except:
             filename = f"video_{uuid.uuid4()}.mp4"

        # Ensure correct extension
        if format == "mp3":
            if not filename.endswith(".mp3"):
                filename = os.path.splitext(filename)[0] + ".mp3"
            # Filesize is likely invalid for mp3 conversion if original was video
            filesize = None 
        elif not filename.endswith(".mp4"):
             filename = os.path.splitext(filename)[0] + ".mp4"

        # 2. Construct yt-dlp command for streaming to stdout
        # -o - : Output to stdout
        cmd = ["yt-dlp", "--no-part", "--no-colors", "--no-check-certificate", "--quiet"]

        # Add deno JS runtime if available (required for modern YouTube extraction)
        deno_path = get_deno_path()
        if deno_path:
            cmd.extend(["--js-runtimes", f"deno:{deno_path}"])
            logger.info(f"Using deno JS runtime: {deno_path}")
        else:
            logger.warning("Deno JS runtime not found. YouTube may fail. Install from https://deno.land")

        # Anti-bot: pass cookies
        cookie_file = BASE_DIR / "cookies.txt"
        if cookie_file.exists():
             cmd.extend(["--cookies", str(cookie_file)])
        else:
            browser_name = get_best_browser_for_cmd()
            if browser_name:
                cmd.extend(["--cookies-from-browser", f"{browser_name}"])
        
        cmd.extend([
            "--socket-timeout", "30",
            "--geo-bypass",
            # Fix for SABR streaming 403 issue - use tv/mweb clients which support cookies
            "--extractor-args", "youtube:player_client=tv,mweb"
        ])
        
        if ffmpeg_exe:
             cmd.extend(["--ffmpeg-location", ffmpeg_exe])
        
        if format == "mp3":
             # Audio only, convert to mp3 on the fly
             # For mp3 conversion, we cannot know final size easily, so we omit Content-Length
             cmd.extend(["-f", "bestaudio/best", "-x", "--audio-format", "mp3", "--audio-quality", "0"])
        else:
             # Video
             target_res = quality
             if target_res:
                 if target_res == "1080p":
                      cmd.extend(["-f", "bestvideo[height<=1080]+bestaudio/best"])
                 elif target_res == "720p":
                      cmd.extend(["-f", "bestvideo[height<=720]+bestaudio/best"])
                 elif target_res == "480p":
                      cmd.extend(["-f", "bestvideo[height<=480]+bestaudio/best"])
                 elif target_res == "360p":
                      cmd.extend(["-f", "bestvideo[height<=360]+bestaudio/best"])
                 else:
                      cmd.extend(["-f", "best"])
             else:
                 cmd.extend(["-f", "best"])

        cmd.extend(["-o", "-", url_str])
        
        # Log command
        logger.info(f"Streaming command: {' '.join(cmd)}")

        # 3. Create Generator
        async def iter_stream():
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Read stdout
            while True:
                chunk = await process.stdout.read(64 * 1024) # 64KB chunks
                if not chunk:
                    break
                yield chunk
            
            await process.wait()
            if process.returncode != 0:
                 err = await process.stderr.read()
                 logger.error(f"Stream error: {err.decode()}")

        # 4. Return Response
        media_type = "audio/mpeg" if format == "mp3" else "video/mp4"
        
        # Proper header encoding for non-ASCII filenames (RFC 5987)
        encoded_filename = quote(filename)
        headers = {
            "Content-Disposition": f"attachment; filename*=utf-8''{encoded_filename}"
        }
        
        if filesize and format != "mp3":
            headers["Content-Length"] = str(filesize)

        return StreamingResponse(
            iter_stream(),
            media_type=media_type,
            headers=headers
        )

    except Exception as e:
        logger.error(f"Stream setup failed: {e}")
        return f"Error: {e}"

@app.post("/video/download")
async def download_video(request: DownloadRequest):
    url_str = str(request.url)
    download_id = str(uuid.uuid4())
    
    # Check for FFmpeg in current directory or PATH
    ffmpeg_exe = "ffmpeg"
    local_ffmpeg = BASE_DIR / "ffmpeg.exe"
    if local_ffmpeg.exists():
        ffmpeg_exe = str(local_ffmpeg)
    elif shutil.which("ffmpeg"):
         ffmpeg_exe = "ffmpeg"
    else:
         ffmpeg_exe = None
    
    try:
        filename = ""
        filepath = ""
        warning_msg = None
        
        # Flag to indicate if we should fallback to yt-dlp
        use_ytdlp_fallback = False
        
        if is_youtube_url(url_str):
            try:
                # --- YOUTUBE DOWNLOAD (PYTUBEFIX) ---
                def download_pytube(download_id):
                    # Try with OAuth allowed to potentially fix bot issues if user authenticates
                    yt = YouTube(url_str, use_oauth=True, allow_oauth_cache=True)
                    stream = None
                    merged_path = None
                    final_res = None
                    
                    if request.format == "mp3":
                        stream = yt.streams.get_audio_only()
                        ext = ".m4a" 
                    else:
                        # VIDEO HANDLING
                        target_res = request.quality
                        
                        # 1. Try Progressive (simplest, fastest)
                        if target_res:
                            stream = yt.streams.filter(res=target_res, progressive=True).first()
                        
                        # 2. Try Adaptive (DASH) + Merge if Progressive failed and FFmpeg available
                        if not stream and ffmpeg_exe and target_res:
                             # Find video only stream
                             video_stream = yt.streams.filter(res=target_res, adaptive=True).first()
                             
                             if video_stream:
                                 audio_stream = yt.streams.get_audio_only()
                                 if audio_stream:
                                     # Download parts
                                     logger.info(f"Downloading adaptive streams: {video_stream.resolution} video + audio")
                                     v_name = f"v_{download_id}_{video_stream.resolution}.mp4"
                                     a_name = f"a_{download_id}.m4a"
                                     
                                     v_path = video_stream.download(output_path=str(DOWNLOADS_DIR), filename=v_name)
                                     a_path = audio_stream.download(output_path=str(DOWNLOADS_DIR), filename=a_name)
                                     
                                     # Merge
                                     out_name = f"{download_id}.mp4"
                                     out_path = DOWNLOADS_DIR / out_name
                                     
                                     cmd = [
                                         ffmpeg_exe, "-y",
                                         "-i", v_path,
                                         "-i", a_path,
                                         "-c:v", "copy",
                                         "-c:a", "aac", 
                                         str(out_path)
                                     ]
                                     
                                     if os.name == 'nt':
                                         # Hide console window on Windows
                                         si = subprocess.STARTUPINFO()
                                         si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                                         subprocess.check_call(cmd, startupinfo=si)
                                     else:
                                         subprocess.check_call(cmd)
                                         
                                     # Cleanup
                                     try:
                                        os.remove(v_path)
                                        os.remove(a_path)
                                     except: pass
                                     
                                     return str(out_path), video_stream.resolution
    
                        # 3. Fallback to Highest Progressive
                        if not stream:
                            stream = yt.streams.get_highest_resolution() 
                        if not stream: 
                            stream = yt.streams.filter(progressive=True).first()
                            
                        ext = ".mp4"
                    
                    if not stream: raise Exception("No suitable stream found")
                    
                    # Download Progressive / Audio
                    out_path = stream.download(output_path=str(DOWNLOADS_DIR), filename=f"{download_id}{ext}")
                    # For audio downloads, resolution is None, maybe use bitrate?
                    res = stream.resolution if hasattr(stream, 'resolution') else "audio"
                    return out_path, res
    
                filepath, actual_quality = await asyncio.get_event_loop().run_in_executor(executor, download_pytube, download_id)
                filename = os.path.basename(filepath)
                
                # Simple Rename for mp3 request (if user really wants .mp3 extension primarily)
                if request.format == "mp3" and not filename.endswith(".mp3"):
                    new_path = os.path.splitext(filepath)[0] + ".mp3"
                    os.rename(filepath, new_path)
                    filepath = new_path
                    filename = os.path.basename(new_path)
    
                if request.quality and actual_quality and actual_quality != request.quality and request.format != "mp3":
                     warning_msg = f"Requested {request.quality} not available. Downloaded {actual_quality} instead."
            
            except Exception as e:
                logger.warning(f"Pytubefix failed: {e}. Falling back to yt-dlp.")
                use_ytdlp_fallback = True

        if not is_youtube_url(url_str) or use_ytdlp_fallback:
            # --- FACEBOOK/OTHER/YOUTUBE FALLBACK DOWNLOAD (YT-DLP) ---
            has_ffmpeg = ffmpeg_exe is not None
            ydl_opts = {
                'outtmpl': str(DOWNLOADS_DIR / f'{download_id}.%(ext)s'),
                'quiet': False,
                'ffmpeg_location': ffmpeg_exe if ffmpeg_exe else None,
                # Anti-bot options
                **get_cookie_kwargs(),
                'nocheckcertificate': True,
                'socket_timeout': 30,
            }
            
            # Simple configuration for robustness
            if request.format == "mp3":
                if has_ffmpeg:
                    ydl_opts['format'] = 'bestaudio/best'
                    ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]
                else:
                    ydl_opts['format'] = 'bestaudio/best' # Will likely download m4a/webm
            else:
                 ydl_opts['format'] = 'best' # Let yt-dlp decide best single file for generic sites

            def download_ytdlp():
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url_str, download=True)
                    return ydl.prepare_filename(info)

            # Run download
            initial_filepath = await asyncio.get_event_loop().run_in_executor(executor, download_ytdlp)
            
            # yt-dlp might change extension
            # Find the file that starts with download_id
            found_file = None
            for f in DOWNLOADS_DIR.glob(f"{download_id}.*"):
                found_file = str(f)
                break
                
            if found_file:
                filepath = found_file
                filename = os.path.basename(filepath)
                # If mp3 requested but no ffmpeg, we might have m4a. Rename if desired, but risky. 
                # Let's keep original ext to be safe.
            else:
                 # fallback if simple glob failed (maybe filename didn't use id?)
                 filepath = initial_filepath
                 filename = os.path.basename(filepath)

        if not os.path.exists(filepath):
            raise Exception("File not found after download")

        response_data = {
            "download_id": download_id,
            "filename": filename,
            "filepath": filepath, # Absolute path on local PC
            "filesize": os.path.getsize(filepath),
            "is_saved_locally": True,
            "local_path": str(filepath) 
        }
        
        if warning_msg:
            response_data["warning"] = warning_msg

        return {
            "success": True,
            "data": response_data
        }

    except Exception as e:
        logger.error(f"Download invalid: {e}")
        raise HTTPException(status_code=400, detail=f"Download failed: {str(e)}")

@app.get("/video/file/{filename}")
async def get_file(filename: str):
    # Try finding in Downloads dir
    file_path = DOWNLOADS_DIR / filename
    if not file_path.exists():
         raise HTTPException(status_code=404, detail="File not found")
    
    # Force attachment to ensure download behavior across browsers
    return FileResponse(
        path=file_path, 
        filename=filename, 
        media_type='application/octet-stream',
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "mode": "Hybrid (Pytubefix + yt-dlp)"}

if __name__ == "__main__":
    import uvicorn
    import webbrowser
    webbrowser.open("http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
