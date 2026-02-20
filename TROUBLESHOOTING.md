# Troubleshooting Guide

## Common Issues

### 1. Internal Server Error (500)
If you see an "Internal Server Error" or the download fails immediately:
1.  Check the `server.log` file in the same folder as the application.
2.  Open it with Notepad and look for the latest "Error" or "CRITICAL" entry.
3.  Common causes:
    *   **Missing FFmpeg**: Ensure `ffmpeg.exe` is in the same folder as `Video Downloader.exe`.
    *   **Internet Connection**: `yt-dlp` requires an active connection.

### 2. Windows Defender / Antivirus Blocking
Windows Defender may flag this application because it is not digitally signed (which costs money).
**To run it safely:**
1.  Right-click `Video Downloader.exe`.
2.  Select **Properties**.
3.  Check **Unblock** at the bottom of the General tab (if visible).
4.  Click **Apply** and **OK**.
5.  If it is quarantined, go to **Windows Security > Virus & threat protection > Protection history**, find the blocked item, and select **Actions > Restore**.

### 3. Application Closes Immediately
The application is designed to run with a console window. If it closes instantly:
1.  Run it from `Powershell` or `CMD` to see the output.
2.  Check `server.log` for startup errors.
