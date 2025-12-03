# Deployment Guide for Render

## สิ่งที่ต้องทำก่อน Deploy:

### 1. Build React App (ทดสอบก่อน)

```bash
npm run build
```

คำสั่งนี้จะสร้างโฟลเดอร์ `dist/` ที่มี static files ของ React

### 2. Git Commit & Push

```bash
git add .
git commit -m "Add React frontend with production build setup"
git push origin main
```

---

## การตั้งค่าบน Render:

### 1. สร้าง Web Service ใหม่

- เลือก "New +" → "Web Service"
- เชื่อมต่อ GitHub repository ของคุณ

### 2. ตั้งค่า Build & Start Commands

**Build Command:**

```bash
./build.sh
```

**Start Command:**

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 3. Environment Variables

ตั้งค่าใน Render Dashboard:

- `GROQ_API_KEY` = your_groq_api_key
- `GEMINI_API_KEY` = your_gemini_api_key
- `PORT` = 10000 (หรือปล่อยให้ Render ตั้งค่าอัตโนมัติ)

### 4. ตั้งค่าอื่นๆ

- **Instance Type**: Free (หรือตามที่ต้องการ)
- **Branch**: main
- **Environment**: Python 3

---

## การทดสอบในเครื่อง (Production Mode)

### 1. Build React

```bash
npm run build
```

### 2. Run Python Server

```bash
python main.py
```

### 3. เปิดเบราว์เซอร์

```
http://localhost:10000
```

ตอนนี้จะเห็น React app ที่ build แล้ว (ไม่ใช่ dev mode)

---

## โครงสร้างไฟล์หลัง Deploy:

```
my-ai-web/
├── dist/              ← React build files (สร้างจาก npm run build)
│   ├── index.html
│   └── assets/
├── src/               ← React source code
├── main.py            ← FastAPI backend (serve dist/)
├── build.sh           ← Render build script
├── requirements.txt   ← Python dependencies
└── package.json       ← Node dependencies
```

---

## สิ่งที่เปลี่ยนไปใน main.py:

✅ รองรับการ serve static files จาก `dist/`
✅ CORS เปิดกว้างสำหรับ production
✅ Mount `/assets` สำหรับ JS/CSS files
✅ Fallback ไปหา index.html เก่าถ้าไม่มี dist

---

## Troubleshooting:

### ถ้า deploy แล้วหน้าเว็บขาว:

1. ตรวจสอบว่า build.sh รันสำเร็จหรือไม่
2. ตรวจสอบว่ามีโฟลเดอร์ `dist/` หรือไม่
3. ดู logs บน Render

### ถ้า API ไม่ทำงาน:

1. ตรวจสอบ Environment Variables (GROQ_API_KEY, GEMINI_API_KEY)
2. ดู logs เพื่อหา error messages

---

## คำสั่งที่มีประโยชน์:

```bash
# Build React app
npm run build

# Run production server locally
python main.py

# Check if dist folder exists
ls -la dist/

# Remove build files (if needed)
rm -rf dist/
```
