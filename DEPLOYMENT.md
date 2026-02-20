# Deployment Guide

This project is now ready for deployment on cloud platforms like **Render** or **Heroku**.

## 1. Prepare for Deployment
The project has been updated to support "Server Mode". When running on a server:
- Files are downloaded to a temporary directory.
- Files are streamed to the user and then automatically deleted to save space.
- The `index.html` is served from the root.

## 2. Deploy to Render (Recommended - Free)
Render is the easiest way to host this for free.

1.  **Push to GitHub**:
    - Create a new repository on GitHub.
    - Push your code to it:
      ```bash
      git init
      git add .
      git commit -m "Deployment ready"
      git branch -M main
      git remote add origin <your-repo-url>
      git push -u origin main
      ```

2.  **Create Service on Render**:
    - Go to [dashboard.render.com](https://dashboard.render.com).
    - Click **New +** -> **Web Service**.
    - Connect your GitHub repository.
    - Render will automatically detect the `render.yaml` or `requirements.txt`.
    - **Environment Variables**: ensure you add:
      - `SERVER_ENV`: `true`

3.  **Deploy**:
    - Click **Create Web Service**.
    - Wait for the build to finish.
    - Your app will be live at `https://your-app-name.onrender.com`.

## 3. Custom Domain Setup
To use your own domain (e.g., `downloader.com`):

1.  **On Render**:
    - Go to **Settings** > **Custom Domains**.
    - Click **Add Custom Domain** and enter `yourdomain.com`.
    - Render will give you DNS records to add.

2.  **On Your Domain Registrar (Run at Namecheap/GoDaddy/Cloudflare)**:
    - Add a **CNAME** record:
        - **Host**: `www` (or `@` for root)
        - **Value**: `your-app-name.onrender.com`
    - Wait up to 24 hours for propagation.

## 4. HTTPS
Render automatically handles HTTPS certificates for you. Once your domain is verified, it will just work securely.

## 5. Security & Performance
- **Rate Limiting**: The current setup uses a basic server. For heavy traffic, consider using Cloudflare in front of your domain.
- **Bot Protection**: We have improved the backend to use `yt-dlp` which is more resilient to bot detection.
- **Cleanup**: The server automatically deletes downloaded files after they are sent to the user to prevent the server from filling up.
