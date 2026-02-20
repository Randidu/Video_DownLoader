# Deployment Guide (Sinhala) - Railway (Backend) & Vercel (Frontend)

ඔබ බලාපොරොත්තු වූ පරිදි, backend එක Railway එකෙත්, frontend එක Vercel එකෙත් දාන විදිහ පහත දැක්වේ.

---

## 1. Backend එක Railway වලට (Python Server)

1. **GitHub වෙත යන්න**: ඔබේ Repo එක (`Randidu/Video_DownLoader`) දැනටමත් යාවත්කාලීන වී ඇත.
2. **Railway Dashboard**:
   - [railway.app](https://railway.app) එකට ගොස් GitHub හරහා Login වන්න.
   - **"New Project"** -> **"Deploy from GitHub repo"** තෝරන්න.
   - ඔබේ `Video_DownLoader` repo එක තෝරන්න.
   - **"Deploy Now"** ඔබන්න.

3. **Settings හදන්න**:
   - Project එක open කරලා **"Settings"** tab එකට යන්න.
   - **"Build Command"**: `pip install -r requirements.txt` (මේක default එනවා).
   - **"Start Command"**: `uvicorn main:app --host 0.0.0.0 --port $PORT` (මේක අනිවාර්යයෙන් දාන්න ඕන).
   - **"Variables"** වලට යන්න.
     - `SERVER_ENV` = `true` ලෙස දාන්න.

4. **Public Domain හදන්න**:
   - **"Settings"** -> **"Networking"** යටතේ **"Generate Domain"** ඔබන්න.
   - එවිට ඔබට URL එකක් ලැබෙනු ඇත (උදා: `https://web-production-xxxx.up.railway.app`).
   - එම URL එක copy කරගන්න. (මෙය Backend URL එකයි).

---

## 2. Frontend එක Vercel වලට (React App)

1. **Vercel Dashboard**:
   - [vercel.com](https://vercel.com) එකට ගොස් GitHub හරහා Login වන්න.
   - **"Add New"** -> **"Project"** තෝරන්න.
   - ඔබේ `Video_DownLoader` repo එක තෝරන්න.

2. **Frontend Settings හදන්න (වැදගත්ම කොටස)**:
   - **"Root Directory"** එකට `Edit` ඔබලා `frontend` ෆෝල්ඩරය තෝරන්න. (මුළු repo එකම නෙවෙයි).
   - **"Build & Output Settings"**: `Vite` අපේක්ෂිත පරිදි detect කරගනීවි (`npm run build`).

3. **Environment Variables**:
   - **"Environment Variables"** කොටසට යන්න.
   - Key: `VITE_API_URL`
   - Value: (ඔබ කලින් Railway එකෙන් ගත් Backend URL එක මෙතන paste කරන්න. අන්තිමට `/` කෑල්ල නැතුව).
     - උදා: `https://web-production-xxxx.up.railway.app`

4. **Deploy**:
   - **"Deploy"** button එක ඔබන්න.
   - ටික වෙලාවකින් ඔබේ Frontend එක live වෙයි!

---

## 3. Domain Connect කිරීම (Porkbun)

දැන් ඔබට Vercel එකෙන් ලැබුණු URL එක ඔබේ Domain එකට (`infinitygrab.xyz`) සම්බන්ධ කළ හැක.

1. **Vercel Settings**:
   - Project එකේ **Settings** -> **Domains** වෙත යන්න.
   - `infinitygrab.xyz` type කර Add කරන්න.
   - Vercel ලබා දෙන `A Record` (IP එක `76.76.21.21`) සහ `CNAME` (`cname.vercel-dns.com`) එක Porkbun DNS වලට දාන්න.

සුබ පැතුම්! දැන් ඔබේ වෙබ් අඩවිය සම්පූර්ණයෙන්ම වැඩ!
