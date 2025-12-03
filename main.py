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

# --- Config Keys ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
vision_model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        vision_model = genai.GenerativeModel('gemini-2.0-flash') # หรือ 1.5-pro
    except: pass

# 🔥🔥🔥 ปรับความโหดตรงนี้ (เลือกก็อปจากด้านบนมาเปลี่ยนได้) 🔥🔥🔥
AI_SYSTEM_PROMPT = """
คุณคือ 'AI ปากแจ๋ว' บอทอัจฉริยะที่ฝีปากกล้าและกวนตีนที่สุด 🤬🔥
- **นิสัย:** ขี้แซะ, กวนประสาท, ใช้ภาษาวัยรุ่น (ตึงๆ, จารย์, หยอกๆ), เป็นกันเองแบบเพื่อนสนิท
- **กฎเหล็ก:**
  1. ห้ามตอบแบบหุ่นยนต์น่าเบื่อ! ต้องใส่อารมณ์ ใส่ความกวนลงไป 🤪
  2. ถ้าคำถามง่ายๆ ให้แซะก่อนตอบ (เช่น "ถามจริง? แค่นี้ไม่รู้? เอ้า ฟังนะ...")
  3. ใช้อิโมจิกวนๆ เยอะๆ (🙄, 🤣, 🤌, 💀, 🤡)
  4. **สำคัญ:** ถึงจะปากดี แต่ข้อมูลต้องเป๊ะและถูกต้องเสมอ!
"""

class QueryRequest(BaseModel):
    prompt: str
    image: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except: return "Error"

@app.post("/calculate")
async def calculate_logic(request: QueryRequest):
    try:
        # 📸 Vision (Gemini)
        if request.image:
            if not vision_model: return {"result": "Error Gemini"}
            try:
                image_data = base64.b64decode(request.image.split(",")[1])
                image = Image.open(io.BytesIO(image_data))
                prompt_text = request.prompt if request.prompt else "รูปนี้คืออะไร"
                
                # ส่งความกวนไปให้ Gemini ด้วย
                full_prompt = f"{AI_SYSTEM_PROMPT}\n\nโจทย์รูปภาพ (ตอบกวนๆ หน่อย): {prompt_text}"
                response = vision_model.generate_content([full_prompt, image])
                return {"result": response.text}
            except Exception as e: return {"result": str(e)}

        # 📝 Text (Llama 3.3)
        else:
            if not groq_client: return {"result": "Error Groq"}
            
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": AI_SYSTEM_PROMPT},
                    {"role": "user", "content": request.prompt}
                ],
                model="llama-3.3-70b-versatile",
                # 🔥 ปรับตรงนี้ให้โหดขึ้น! (0.5 = ปกติ, 0.9 = สร้างสรรค์/กวน, 1.2 = หลุดโลก)
                temperature=0.9, 
                max_tokens=1024,
            )
            return {"result": chat_completion.choices[0].message.content}
        
    except Exception as e:
        return {"result": f"Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)