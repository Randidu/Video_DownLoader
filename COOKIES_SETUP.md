# How to Fix "Sign in to confirm you’re not a bot" Error

This error happens because YouTube is blocking automated requests from your IP or browser session. To fix this, you need to provide your YouTube login cookies to the application.

## Method 1: Use `cookies.txt` (Recommended)

This method is the most reliable.

1.  **Install a Cookie Export Extension**:
    *   **Chrome/Edge/Brave**: Install "Get cookies.txt LOCALLY" (or similar).
    *   **Firefox**: Install "cookies.txt".

2.  **Log in to YouTube**:
    *   Open your browser and go to [YouTube.com](https://www.youtube.com).
    *   Log in with your Google account.

3.  **Export Cookies**:
    *   Click the extension icon while on the YouTube tab.
    *   Click "Export" or "Download".
    *   Save the file as `cookies.txt`.

4.  **Place the File**:
    *   Move the `cookies.txt` file to the root folder of this project:
        `c:\Users\randi\OneDrive\Desktop\youtube video downloader\cookies.txt`

5.  **Restart the App**:
    *   The application will automatically detect this file and use it.

## Method 2: Browser Cookies (Automatic)

The application tries to pull cookies from your installed browsers automatically. However, this often fails if the browser locks the cookie database (common when the browser is open).

*   **Close your browser** completely and try running the downloader again.
*   Ensure you are logged into YouTube on your default browser (Chrome, Edge, Firefox, etc.).

## Troubleshooting

You can run the included test script to see if your cookies are being detected:

1.  Open a terminal in the project folder.
2.  Run:
    ```bash
    python test_cookies.py
    ```
3.  It will tell you if `cookies.txt` is found or if browser cookies are available.
