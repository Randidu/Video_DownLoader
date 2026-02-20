# Deployment Guide for infinitygrab.xyz

## 1. Deploy to Render (First Step)
If you haven't created the service on Render yet:
1.  Go to [dashboard.render.com](https://dashboard.render.com).
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub repo: `Randidu/Video_DownLoader`.
4.  **Settings**:
    -   **Name**: `infinitygrab`
    -   **Runtime**: `Python 3`
    -   **Build Command**: `pip install -r requirements.txt`
    -   **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
    -   **Environment Variables**: Add `SERVER_ENV` = `true`.
5.  Click **Create Web Service**.

---

## 2. Connect Domain (Porkbun + Render)

Once your Render service is live (you see a green "Live" badge), follow these steps to connect `infinitygrab.xyz`.

### Step A: Get DNS Info from Render
1.  In your Render Dashboard, go to your service's **Settings**.
2.  Scroll down to **Custom Domains**.
3.  Click **Add Custom Domain**.
4.  Enter `infinitygrab.xyz` and click **Save**.
5.  Render will verify it. It will tell you to add an **A Record** pointing to an IP address (usually `216.24.57.1`).
6.  Click **Add Custom Domain** again and enter `www.infinitygrab.xyz`.
7.  Render will tell you to add a **CNAME Record** pointing to your unique Render URL (e.g., `infinitygrab.onrender.com`).

### Step B: Configure Porkbun DNS
1.  Log in to your **Porkbun Account**.
2.  Go to **Domain Management**.
3.  Find `infinitygrab.xyz` and click **DNS** (or "Edit" -> "DNS Records").
4.  **Delete** any existing records that say "Parking" or "Porkbun".

5.  **Add the Root Record (for infinitygrab.xyz)**:
    -   **Type**: `A`
    -   **Host**: `@` (leave blank if Porkbun doesn't accept @)
    -   **Answer/Value**: `216.24.57.1` (Copy the IP from Render to be sure!)
    -   Click **Add**.

6.  **Add the WWW Record (for www.infinitygrab.xyz)**:
    -   **Type**: `CNAME`
    -   **Host**: `www`
    -   **Answer/Value**: `infinitygrab.onrender.com` (Your Render app URL)
    -   Click **Add**.

### Step C: Wait
-   DNS changes can take 5 minutes to 1 hour to propagate.
-   Render will automatically generate an SSL certificate (HTTPS) for you.
-   Once the "Verifying..." status on Render turns green, your site `https://infinitygrab.xyz` is live!
