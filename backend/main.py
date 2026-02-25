"""
InfinityGrab - Backend API Server
Supports YouTube, Facebook, TikTok, Instagram, and 1000+ sites.
"""

# ─────────────────────────────────────────────────────────────
# Standard Library Imports
# ─────────────────────────────────────────────────────────────
import asyncio
import base64
import logging
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional
from urllib.parse import quote

# ─────────────────────────────────────────────────────────────
# Third-Party Imports
# ─────────────────────────────────────────────────────────────
import yt_dlp
from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl
from pytubefix import YouTube


# ─────────────────────────────────────────────────────────────
# Paths & Base Directory
# ─────────────────────────────────────────────────────────────

# Works for both "python main.py" and PyInstaller .exe
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent.resolve()

STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)


# ─────────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────────

log_file_path = BASE_DIR / "server.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file_path, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logging.getLogger("multipart").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

logger.info(f"Base Directory : {BASE_DIR}")
logger.info(f"Static Dir     : {STATIC_DIR}")


# ─────────────────────────────────────────────────────────────
# Environment Detection (Server vs Desktop)
# ─────────────────────────────────────────────────────────────

IS_SERVER = bool(
    os.environ.get("RAILWAY_ENVIRONMENT")
    or os.environ.get("RENDER")
    or os.environ.get("DYNO")
    or os.environ.get("SERVER_ENV")
)

if IS_SERVER:
    DOWNLOADS_DIR = Path(tempfile.gettempdir()) / "infinitygrab_downloads"
    logger.info(f"Mode: SERVER  |  Downloads: {DOWNLOADS_DIR}")
else:
    DOWNLOADS_DIR = Path.home() / "Downloads"
    logger.info(f"Mode: DESKTOP |  Downloads: {DOWNLOADS_DIR}")

DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────────────────────
# Cookie Management
# ─────────────────────────────────────────────────────────────

COOKIES_FILE = BASE_DIR / "cookies.txt"


def restore_cookies_from_env() -> bool:
    """Restore cookies.txt from the YOUTUBE_COOKIES base64 environment variable."""
    cookies_b64 = os.environ.get("YOUTUBE_COOKIES")
    if not cookies_b64:
        return False
    try:
        decoded = base64.b64decode(cookies_b64.strip())
        COOKIES_FILE.write_bytes(decoded)
        logger.info(f"✅ Cookies restored from env ({len(decoded)} bytes)")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to decode YOUTUBE_COOKIES: {e}")
        return False


cookies_restored = restore_cookies_from_env()


def get_cookie_options() -> dict:
    """Return yt-dlp cookie options: prefers cookies.txt, falls back to browser."""
    if COOKIES_FILE.exists():
        logger.info(f"Using cookies file: {COOKIES_FILE}")
        return {"cookiefile": str(COOKIES_FILE)}

    browser = detect_browser()
    if browser:
        logger.info(f"Using browser cookies: {browser}")
        return {"cookiesfrombrowser": (browser,)}

    return {}


def detect_browser() -> Optional[str]:
    """Detect an installed browser to pull cookies from."""
    if platform.system() == "Windows":
        browser_paths = {
            "chrome": os.path.expandvars(r"%LocalAppData%\Google\Chrome\User Data"),
            "edge": os.path.expandvars(r"%LocalAppData%\Microsoft\Edge\User Data"),
            "firefox": os.path.expandvars(r"%AppData%\Mozilla\Firefox\Profiles"),
            "brave": os.path.expandvars(r"%LocalAppData%\BraveSoftware\Brave-Browser\User Data"),
        }
    else:
        home = Path.home()
        browser_paths = {
            "chrome": str(home / ".config/google-chrome"),
            "chromium": str(home / ".config/chromium"),
            "firefox": str(home / ".mozilla/firefox"),
        }

    for browser, path in browser_paths.items():
        if os.path.exists(path):
            return browser
    return None


# ─────────────────────────────────────────────────────────────
# FFmpeg & Deno Helpers
# ─────────────────────────────────────────────────────────────

def find_ffmpeg() -> Optional[str]:
    """Locate ffmpeg: local .exe → PATH → None."""
    local = BASE_DIR / "ffmpeg.exe"
    if local.exists():
        return str(local)
    if shutil.which("ffmpeg"):
        return "ffmpeg"
    return None


def find_deno() -> Optional[str]:
    """Locate deno runtime for modern YouTube signature decryption."""
    local = Path.home() / ".deno" / "bin" / "deno.exe"
    if local.exists():
        return str(local)
    return shutil.which("deno")


# ─────────────────────────────────────────────────────────────
# FastAPI App
# ─────────────────────────────────────────────────────────────

app = FastAPI(
    title="InfinityGrab API",
    description="Download videos from YouTube, Facebook, TikTok, Instagram & 1000+ sites.",
    version="2.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve built frontend assets from static/assets
assets_path = STATIC_DIR / "assets"
assets_path.mkdir(exist_ok=True)
app.mount("/assets", StaticFiles(directory=str(assets_path)), name="assets")

# Thread pool for blocking I/O
executor = ThreadPoolExecutor(max_workers=4)


# ─────────────────────────────────────────────────────────────
# Pydantic Models
# ─────────────────────────────────────────────────────────────

class VideoURL(BaseModel):
    url: HttpUrl


class DownloadRequest(BaseModel):
    url: HttpUrl
    format: str = "best"
    quality: Optional[str] = None


# ─────────────────────────────────────────────────────────────
# Static File Routes
# ─────────────────────────────────────────────────────────────

def _serve_static(filename: str):
    path = STATIC_DIR / filename
    if path.exists():
        return FileResponse(str(path))
    raise HTTPException(status_code=404, detail=f"{filename} not found")


@app.get("/", include_in_schema=False)
async def root():
    return _serve_static("index.html")


@app.get("/logo.png", include_in_schema=False)
async def serve_logo():
    return _serve_static("logo.png")


@app.get("/favicon.ico", include_in_schema=False)
async def serve_favicon():
    path = STATIC_DIR / "favicon.ico"
    if path.exists():
        return FileResponse(str(path))
    return await serve_logo()  # fallback


@app.get("/manifest.json", include_in_schema=False)
async def serve_manifest():
    return _serve_static("manifest.json")


@app.get("/robots.txt", include_in_schema=False)
async def serve_robots():
    return _serve_static("robots.txt")


@app.get("/sitemap.xml", include_in_schema=False)
async def serve_sitemap():
    return _serve_static("sitemap.xml")


@app.get("/ads.txt", include_in_schema=False)
async def serve_ads_txt():
    return _serve_static("ads.txt")


# ─────────────────────────────────────────────────────────────
# Debug Routes
# ─────────────────────────────────────────────────────────────

@app.get("/health", tags=["Status"])
async def health_check():
    """Check server health and mode."""
    return {
        "status": "healthy",
        "mode": "server" if IS_SERVER else "desktop",
        "engine": "Pytubefix + yt-dlp",
    }


@app.get("/debug/cookies", tags=["Status"])
async def debug_cookies():
    """Verify cookie status on the server."""
    return {
        "cookies_env_found": bool(os.environ.get("YOUTUBE_COOKIES")),
        "cookies_file_exists": COOKIES_FILE.exists(),
        "cookies_file_size": COOKIES_FILE.stat().st_size if COOKIES_FILE.exists() else 0,
        "cookies_restored_on_startup": cookies_restored,
        "is_server": IS_SERVER,
        "base_dir": str(BASE_DIR),
    }


# ─────────────────────────────────────────────────────────────
# Video Info Route
# ─────────────────────────────────────────────────────────────

@app.post("/video/info", tags=["Video"])
async def get_video_info(video: VideoURL):
    """Fetch metadata for a video URL (title, thumbnail, duration, etc.)."""
    url_str = str(video.url)

    def _fetch_info():
        opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
            "format": None,
            "nocheckcertificate": True,
            "ignoreerrors": False,
            "socket_timeout": 30,
        }
        cookie_opts = get_cookie_options()
        try:
            with yt_dlp.YoutubeDL({**opts, **cookie_opts}) as ydl:
                return ydl.extract_info(url_str, download=False)
        except Exception as e:
            logger.warning(f"yt-dlp info with cookies failed: {e}. Retrying anonymously.")
            with yt_dlp.YoutubeDL(opts) as ydl:
                return ydl.extract_info(url_str, download=False)

    try:
        info = await asyncio.get_event_loop().run_in_executor(executor, _fetch_info)
        return {
            "success": True,
            "data": {
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "duration": info.get("duration"),
                "uploader": info.get("uploader"),
                "view_count": info.get("view_count"),
            },
        }
    except Exception as e:
        logger.error(f"Video info error: {e}")
        raise HTTPException(status_code=400, detail=str(e))


# ─────────────────────────────────────────────────────────────
# Streaming Download Route (GET)
# ─────────────────────────────────────────────────────────────

@app.get("/video/download_link", tags=["Video"])
async def stream_download(
    url: str,
    background_tasks: BackgroundTasks,
    format: str = "best",
    quality: Optional[str] = None,
):
    """Stream a video/audio directly to the browser for download."""
    url_str = url
    ffmpeg_exe = find_ffmpeg()

    # --- Fetch filename & filesize ---
    def _get_meta():
        opts = {"quiet": True, "no_warnings": True, "nocheckcertificate": True}
        cookie_opts = get_cookie_options()
        try:
            with yt_dlp.YoutubeDL({**opts, **cookie_opts}) as ydl:
                info = ydl.extract_info(url_str, download=False)
                return ydl.prepare_filename(info), info.get("filesize") or info.get("filesize_approx"), True
        except Exception as e:
            logger.warning(f"Meta fetch with cookies failed: {e}. Retrying anonymously.")
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url_str, download=False)
                return ydl.prepare_filename(info), info.get("filesize") or info.get("filesize_approx"), False

    filesize = None
    use_cookies = True
    filename = f"video_{uuid.uuid4()}.mp4"

    try:
        raw_path, filesize, use_cookies = await asyncio.get_event_loop().run_in_executor(executor, _get_meta)
        filename = os.path.basename(raw_path)
    except Exception:
        pass

    # Normalize extension
    if format == "mp3":
        filename = os.path.splitext(filename)[0] + ".mp3"
        filesize = None
    elif not filename.endswith(".mp4"):
        filename = os.path.splitext(filename)[0] + ".mp4"

    # --- Build yt-dlp streaming command ---
    cmd = ["yt-dlp", "--no-part", "--no-colors", "--no-check-certificate", "--quiet"]

    deno_path = find_deno()
    if deno_path:
        cmd.extend(["--js-runtimes", f"deno:{deno_path}"])
        logger.info(f"Deno runtime: {deno_path}")
    else:
        logger.warning("Deno not found. YouTube downloads may fail. Install: https://deno.land")

    # Cookies
    if use_cookies:
        if COOKIES_FILE.exists():
            cmd.extend(["--cookies", str(COOKIES_FILE)])
        else:
            browser = detect_browser()
            if browser:
                cmd.extend(["--cookies-from-browser", browser])

    cmd.extend(["--socket-timeout", "30", "--geo-bypass"])

    if ffmpeg_exe:
        cmd.extend(["--ffmpeg-location", ffmpeg_exe])

    # Format selection
    quality_map = {
        "1080p": "bestvideo[height<=1080]+bestaudio/best",
        "720p": "bestvideo[height<=720]+bestaudio/best",
        "480p": "bestvideo[height<=480]+bestaudio/best",
        "360p": "bestvideo[height<=360]+bestaudio/best",
    }
    if format == "mp3":
        cmd.extend(["-f", "bestaudio/best", "-x", "--audio-format", "mp3", "--audio-quality", "0"])
    elif quality and quality in quality_map:
        cmd.extend(["-f", quality_map[quality]])
    else:
        cmd.extend(["-f", "best"])

    cmd.extend(["-o", "-", url_str])
    logger.info(f"Stream cmd: {' '.join(cmd)}")

    # --- Async generator streaming to client ---
    async def _stream_chunks():
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        while True:
            chunk = await process.stdout.read(64 * 1024)  # 64 KB
            if not chunk:
                break
            yield chunk
        await process.wait()
        if process.returncode != 0:
            err = await process.stderr.read()
            logger.error(f"Stream subprocess error: {err.decode()}")

    media_type = "audio/mpeg" if format == "mp3" else "video/mp4"
    encoded_name = quote(filename)
    headers = {"Content-Disposition": f"attachment; filename*=utf-8''{encoded_name}"}
    if filesize and format != "mp3":
        headers["Content-Length"] = str(filesize)

    return StreamingResponse(_stream_chunks(), media_type=media_type, headers=headers)


# ─────────────────────────────────────────────────────────────
# Local Download Route (POST) — saves to DOWNLOADS_DIR
# ─────────────────────────────────────────────────────────────

def _is_youtube_url(url: str) -> bool:
    u = url.lower()
    return "youtube.com" in u or "youtu.be" in u


@app.post("/video/download", tags=["Video"])
async def download_video(request: DownloadRequest):
    """Download video to server/local disk; returns file path and metadata."""
    url_str = str(request.url)
    download_id = str(uuid.uuid4())
    ffmpeg_exe = find_ffmpeg()
    warning_msg = None
    filepath = ""
    filename = ""

    # ── YouTube path: try Pytubefix first, fall back to yt-dlp ──
    if _is_youtube_url(url_str):
        try:
            def _pytube_download():
                yt = YouTube(url_str, use_oauth=True, allow_oauth_cache=True)
                stream = None
                target_res = request.quality

                if request.format == "mp3":
                    stream = yt.streams.get_audio_only()
                    ext = ".m4a"
                else:
                    # 1. Progressive (has audio + video in one file)
                    if target_res:
                        stream = yt.streams.filter(res=target_res, progressive=True).first()

                    # 2. Adaptive (separate streams) + FFmpeg merge
                    if not stream and ffmpeg_exe and target_res:
                        v_stream = yt.streams.filter(res=target_res, adaptive=True).first()
                        if v_stream:
                            a_stream = yt.streams.get_audio_only()
                            if a_stream:
                                logger.info(f"Adaptive merge: {v_stream.resolution}")
                                v_file = v_stream.download(str(DOWNLOADS_DIR), filename=f"v_{download_id}.mp4")
                                a_file = a_stream.download(str(DOWNLOADS_DIR), filename=f"a_{download_id}.m4a")
                                out = str(DOWNLOADS_DIR / f"{download_id}.mp4")
                                merge_cmd = [ffmpeg_exe, "-y", "-i", v_file, "-i", a_file,
                                             "-c:v", "copy", "-c:a", "aac", out]
                                if os.name == "nt":
                                    si = subprocess.STARTUPINFO()
                                    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                                    subprocess.check_call(merge_cmd, startupinfo=si)
                                else:
                                    subprocess.check_call(merge_cmd)
                                try:
                                    os.remove(v_file)
                                    os.remove(a_file)
                                except Exception:
                                    pass
                                return out, v_stream.resolution

                    # 3. Best available progressive as fallback
                    if not stream:
                        stream = yt.streams.get_highest_resolution()
                    if not stream:
                        stream = yt.streams.filter(progressive=True).first()

                    ext = ".mp4"

                if not stream:
                    raise RuntimeError("No suitable stream found via Pytubefix")

                out = stream.download(str(DOWNLOADS_DIR), filename=f"{download_id}{ext}")
                res = getattr(stream, "resolution", "audio")
                return out, res

            filepath, actual_quality = await asyncio.get_event_loop().run_in_executor(executor, _pytube_download)
            filename = os.path.basename(filepath)

            # Rename .m4a → .mp3 if user asked for mp3
            if request.format == "mp3" and not filename.endswith(".mp3"):
                new_path = os.path.splitext(filepath)[0] + ".mp3"
                os.rename(filepath, new_path)
                filepath, filename = new_path, os.path.basename(new_path)

            if request.quality and actual_quality and actual_quality != request.quality:
                warning_msg = f"Requested {request.quality} not available. Got {actual_quality} instead."

        except Exception as e:
            logger.warning(f"Pytubefix failed: {e}. Falling back to yt-dlp.")
            filepath = ""  # trigger yt-dlp below

    # ── Generic path: yt-dlp (Facebook, TikTok, or YouTube fallback) ──
    if not filepath:
        ydlp_opts = {
            "outtmpl": str(DOWNLOADS_DIR / f"{download_id}.%(ext)s"),
            "quiet": False,
            "nocheckcertificate": True,
            "socket_timeout": 30,
        }
        if ffmpeg_exe:
            ydlp_opts["ffmpeg_location"] = ffmpeg_exe

        if request.format == "mp3":
            ydlp_opts["format"] = "bestaudio/best"
            if ffmpeg_exe:
                ydlp_opts["postprocessors"] = [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}]
        else:
            ydlp_opts["format"] = "best"

        cookie_opts = get_cookie_options()

        def _ytdlp_download():
            try:
                with yt_dlp.YoutubeDL({**ydlp_opts, **cookie_opts}) as ydl:
                    info = ydl.extract_info(url_str, download=True)
                    return ydl.prepare_filename(info)
            except Exception as e:
                logger.warning(f"yt-dlp with cookies failed: {e}. Retrying without.")
                with yt_dlp.YoutubeDL(ydlp_opts) as ydl:
                    info = ydl.extract_info(url_str, download=True)
                    return ydl.prepare_filename(info)

        await asyncio.get_event_loop().run_in_executor(executor, _ytdlp_download)

        # yt-dlp may change the extension — find what was actually saved
        found = next(DOWNLOADS_DIR.glob(f"{download_id}.*"), None)
        filepath = str(found) if found else ""
        filename = os.path.basename(filepath)

    if not filepath or not os.path.exists(filepath):
        raise HTTPException(status_code=500, detail="File not found after download")

    response = {
        "success": True,
        "data": {
            "download_id": download_id,
            "filename": filename,
            "filepath": filepath,
            "filesize": os.path.getsize(filepath),
            "is_saved_locally": True,
        },
    }
    if warning_msg:
        response["data"]["warning"] = warning_msg

    return response


# ─────────────────────────────────────────────────────────────
# File Serve Route (for local/desktop downloads)
# ─────────────────────────────────────────────────────────────

@app.get("/video/file/{filename}", tags=["Video"])
async def serve_file(filename: str):
    """Serve a previously downloaded file from the downloads directory."""
    file_path = DOWNLOADS_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


# ─────────────────────────────────────────────────────────────
# Entry Point (Desktop Mode)
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import webbrowser
    import uvicorn

    webbrowser.open("http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
