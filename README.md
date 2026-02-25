# 🚀 InfinityGrab — Video Downloader

Download videos from YouTube, Facebook, TikTok, Instagram, and 1000+ sites.

---

## 📁 Project Structure

```
Video_DownLoader/
├── backend/                   ← FastAPI Python backend
│   ├── main.py                ← API server entry point
│   ├── requirements.txt       ← Python dependencies
│   ├── static/                ← Served by FastAPI (built frontend + media)
│   │   ├── index.html
│   │   ├── logo.png
│   │   ├── favicon.ico
│   │   ├── manifest.json
│   │   ├── robots.txt
│   │   ├── sitemap.xml
│   │   └── assets/            ← Vite build output (JS/CSS bundles)
│   └── cookies.txt            ← (optional) YouTube auth cookies
│
├── frontend/                  ← React + Vite + TypeScript frontend
│   ├── src/
│   │   ├── components/        ← Reusable UI components
│   │   ├── pages/             ← Route pages
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── index.css
│   │   └── Types.ts
│   ├── public/
│   ├── package.json
│   └── vite.config.ts         ← Builds output → backend/static
│
├── start_backend.bat          ← Run FastAPI backend only
├── start_frontend.bat         ← Run Vite dev server only
├── start_app.bat              ← Build frontend + run full app
└── README.md
```

---

## 🛠️ Setup & Running

### 1. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies
```bash
cd frontend
npm install
```

---

## ▶️ Development Mode

Run both servers simultaneously:

**Terminal 1 — Backend:**
```bash
cd backend
python main.py
# API available at http://localhost:8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
# UI available at http://localhost:5173
```

> Set `VITE_API_URL=http://localhost:8000` in `frontend/.env` during development.

---

## 🏭 Production / Full App

Build the frontend into `backend/static`, then run the FastAPI server:

```bash
# Option 1: One-click Windows script
start_app.bat

# Option 2: Manual
cd frontend && npm run build
cd ../backend && python main.py
# Full app at http://localhost:8000
```

---

## 🌐 Deployment (Railway / Render)

- Entry point: `backend/main.py`
- Set env var `YOUTUBE_COOKIES` (base64 encoded cookies.txt) for YouTube auth
- See `DEPLOYMENT.md` for full deployment guides

---

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `YOUTUBE_COOKIES` | Base64-encoded cookies.txt for YouTube authentication |
| `VITE_API_URL` | Frontend API base URL (for development only) |
| `SERVER_ENV` | Set to any value to enable server mode |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Server health check |
| `POST` | `/video/info` | Fetch video metadata |
| `GET` | `/video/download_link` | Stream video/audio to browser |
| `POST` | `/video/download` | Download to server disk |
| `GET` | `/video/file/{filename}` | Serve a downloaded file |
| `GET` | `/debug/cookies` | Cookie status (debug) |
