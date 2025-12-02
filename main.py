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

# --- 1. ตั้งค่า Groq (สำหรับคุยปกติ - Llama 3.3) ---
# ดึง Key จาก Environment Variable
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY)

# --- 2. ตั้งค่า Gemini (สำหรับดูรูปภาพ) ---
# ดึง Key จาก Environment Variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

vision_model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        # 🔥 แก้ตรงนี้: กลับมาใช้ 1.5 Flash (ตัวเสถียร โควตาเยอะ)
        vision_model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        print(f"Gemini Error: {e}")

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

# ส่วนหลังบ้าน (สมอง AI)
@app.post("/calculate")
async def calculate_logic(request: QueryRequest):
    try:
        # 🔀 กรณีที่ 1: มีรูปภาพส่งมา -> ให้ Gemini ดู
        if request.image:
            print("📸 มีรูปภาพ! ส่งให้ Gemini 1.5 Flash ดู...")
            
            if not vision_model:
                return {"result": "Error: ไม่พบ GEMINI_API_KEY ใน Server (หรือตั้งค่าผิด)"}

            try:
                # แปลงรหัส Base64 กลับเป็นไฟล์รูป
                image_data = base64.b64decode(request.image.split(",")[1])
                image = Image.open(io.BytesIO(image_data))
                
                # ถาม Gemini
                prompt_text = request.prompt if request.prompt else "รูปนี้คืออะไร อธิบายเป็นภาษาไทย"
                response = vision_model.generate_content([prompt_text, image])
                return {"result": response.text}
                
            except Exception as img_err:
                return {"result": f"Error ดูรูปไม่ได้: {str(img_err)}"}

        # 📝 กรณีที่ 2: ข้อความล้วน -> ให้ Groq (Llama 3.3) ตอบ
        else:
            print("📝 ข้อความปกติ: ส่งให้ Llama 3.3 (70B) ตอบ...")
            
            if not GROQ_API_KEY:
                return {"result": "Error: ไม่พบ GROQ_API_KEY ใน Server"}

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