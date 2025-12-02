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

# --- 1. ตั้งค่า Groq (Llama 3.3) ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if GROQ_API_KEY:
    groq_client = Groq(api_key=GROQ_API_KEY)
else:
    groq_client = None

# --- 2. ตั้งค่า Gemini (Gemini 2.0 Flash) ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
vision_model = None

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        # 🔥 ใช้ตัวนี้ครับ 'gemini-2.0-flash' (บัญชีคุณมีสิทธิ์ใช้ตัวนี้)
        vision_model = genai.GenerativeModel('gemini-2.0-flash')
    except Exception as e:
        print(f"Gemini Init Error: {e}")

class QueryRequest(BaseModel):
    prompt: str
    image: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Error: ไม่พบไฟล์ index.html</h1>"

@app.post("/calculate")
async def calculate_logic(request: QueryRequest):
    try:
        # 🔀 กรณีมีรูป: ให้ Gemini 2.0 Flash ดู
        if request.image:
            print("📸 มีรูปภาพ! ส่งให้ Gemini 2.0 Flash...")
            
            if not vision_model:
                return {"result": "Error: ไม่พบ GEMINI_API_KEY หรือตั้งค่าโมเดลผิด"}

            try:
                # แปลงรูป
                image_data = base64.b64decode(request.image.split(",")[1])
                image = Image.open(io.BytesIO(image_data))
                
                # ถาม Gemini
                prompt_text = request.prompt if request.prompt else "รูปนี้คืออะไร อธิบายภาษาไทย"
                response = vision_model.generate_content([prompt_text, image])
                return {"result": response.text}
                
            except Exception as img_err:
                return {"result": f"Error ดูรูปไม่ได้: {str(img_err)}"}

        # 📝 กรณีข้อความล้วน: ให้ Groq ตอบ
        else:
            print("📝 ข้อความปกติ: ส่งให้ Llama 3.3...")
            if not groq_client:
                return {"result": "Error: ไม่พบ GROQ_API_KEY"}

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