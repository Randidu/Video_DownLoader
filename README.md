# 🎥 YouTube & Social Media Video Downloader

A modern, fast, and reliable web application to download videos from YouTube, Facebook, Instagram, TikTok, and more. Built with **FastAPI** (Python) and **Vanilla JS**.

![Banner](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)

---

## 🚀 Quick Start (For Developers)

We have included automated scripts to get you up and running in seconds on Windows.

### 1. Setup
Run **`setup_project.bat`**.
*   Checks for Python.
*   Creates a virtual environment (`venv`).
*   Installs all dependencies.

### 2. Run
Run **`run_project.bat`**.
*   Activates the virtual environment.
*   Starts the backend server.
*   Opens the web interface in your browser automatically.

---

## 📦 Distribution & Deployment

### Create Portable App (.exe)
To create a standalone `.exe` file that runs on any Windows PC without needing Python installed:
1.  Run **`build_app.bat`**.
2.  Find the result in the `dist/Video Downloader` folder.
3.  Zip this folder and share it!

### Deploy to Cloud (Render/Heroku)
This project is cloud-ready.
*   **Source Code**: valid `Procfile`, `render.yaml`, and `requirements.txt` included.
*   **Server Logic**: Handles temp files and cleanup automatically when running on a server.
*   **Guide**: See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions.

---

## 🛠 Manual Setup (Mac/Linux/Terminal)

If you prefer using the terminal or are on a non-Windows OS:

1.  **Clone the repo**:
    ```bash
    git clone <your-repo-url>
    cd video-downloader
    ```

2.  **Create venv**:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run**:
    ```bash
    python main.py
    ```

---

## 🏗 Project Structure

*   `main.py`: The FastAPI backend server.
*   `index.html`: The frontend user interface.
*   `setup_project.bat`: One-click setup script.
*   `build_app.bat`: Script to compile to .exe.
*   `DEPLOYMENT.md`: Cloud hosting guide.
*   `TROUBLESHOOTING.md`: Common error fixes.

## ⚠️ Requirements

*   **Python 3.8+**
*   **FFmpeg**: Only required for high-quality (1080p+) merges locally. Included automatically in the Portable build.

## 📄 License
MIT License. Free to use and modify.

