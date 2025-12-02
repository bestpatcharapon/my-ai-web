import os
import io
import base64
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from groq import Groq
import google.generativeai as genai
from PIL import Image
import uvicorn

app = FastAPI()

# --- API Keys Configuration ---
# ✅ ใช้ Environment Variables เพื่อความปลอดภัย
# ตั้งค่าใน Render: Settings > Environment > Add Variable
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# ตรวจสอบว่ามี API Keys หรือไม่
if not GROQ_API_KEY or not GEMINI_API_KEY:
    print("⚠️ Warning: API Keys not found! Please set environment variables:")
    print("   - GROQ_API_KEY")
    print("   - GEMINI_API_KEY")

# เชื่อมต่อกับ AI Services
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    vision_model = genai.GenerativeModel('gemini-2.0-flash-exp')
else:
    vision_model = None

class QueryRequest(BaseModel):
    prompt: str
    image: Optional[str] = None

# ส่วนหน้าบ้าน (เสิร์ฟไฟล์ HTML)
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Error: ไม่พบไฟล์ index.html (อย่าลืมอัปโหลดขึ้น GitHub นะครับ)</h1>"

# ส่วนหลังบ้าน (สมอง AI สับราง)
@app.post("/calculate")
async def calculate_logic(request: QueryRequest):
    try:
        # 🔀 กรณีมีรูปภาพ: ส่งให้ Gemini 2.0 ดู
        if request.image:
            print("📸 มีรูปภาพ! ให้ Gemini 2.0 Flash ช่วยดู...")
            try:
                # แปลงไฟล์รูป
                image_data = base64.b64decode(request.image.split(",")[1])
                image = Image.open(io.BytesIO(image_data))
                
                # ถาม Gemini
                prompt_text = request.prompt if request.prompt else "รูปนี้คืออะไร อธิบายเป็นภาษาไทย"
                response = vision_model.generate_content([prompt_text, image])
                return {"result": response.text}
                
            except Exception as img_err:
                return {"result": f"Error ดูรูปไม่ได้: {str(img_err)}"}

        # 📝 กรณีข้อความล้วน: ส่งให้ Groq (Llama 3.3) ตอบ
        else:
            print("📝 ข้อความปกติ: ให้ Llama 3.3 (70B) ตอบ...")
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant fluent in Thai."},
                    {"role": "user", "content": request.prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.6,
                max_tokens=1024,
            )
            return {"result": chat_completion.choices[0].message.content}
        
    except Exception as e:
        return {"result": f"Error ระบบ: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)