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
        vision_model = genai.GenerativeModel('gemini-1.5-flash-001') # หรือ 2.0-flash
    except: pass

# 🔥 ปรับจูนใหม่: สูตร "กลมกล่อม" (Natural & Fun)
AI_SYSTEM_PROMPT = """
คุณคือ 'Best Bot' เพื่อนคู่คิด AI ที่ฉลาดและนิสัยดี 🤖
- **สไตล์การตอบ:** เป็นกันเอง เหมือนคุยกับเพื่อนที่ฉลาดๆ ใช้ภาษาพูดได้ (แต่ไม่หยาบคาย)
- **การใช้อิโมจิ:** ให้ใส่บ้างพอให้ดูมีชีวิตชีวา (เช่น ท้ายประโยค หรือตรงจุดสำคัญ) **แต่ห้ามใส่เยอะเกินไปจนดูเลอะเทอะ** เอาแค่พองาม ✨
- **กฎการตอบ:**
  1. ตอบให้ตรงคำถาม กระชับ ได้ใจความ
  2. ถ้าเรื่องไหนยาก ให้อธิบายเปรียบเทียบง่ายๆ
  3. ให้กำลังใจผู้ใช้เสมอ ถ้าเขาดูเครียด
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
        # 📸 Vision
        if request.image:
            if not vision_model: return {"result": "Error Gemini"}
            try:
                image_data = base64.b64decode(request.image.split(",")[1])
                image = Image.open(io.BytesIO(image_data))
                prompt_text = request.prompt if request.prompt else "รูปนี้คืออะไร"
                
                full_prompt = f"{AI_SYSTEM_PROMPT}\n\nโจทย์รูปภาพ: {prompt_text}"
                response = vision_model.generate_content([full_prompt, image])
                return {"result": response.text}
            except Exception as e: return {"result": str(e)}

        # 📝 Text
        else:
            if not groq_client: return {"result": "Error Groq"}
            
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": AI_SYSTEM_PROMPT},
                    {"role": "user", "content": request.prompt}
                ],
                model="llama-3.3-70b-versatile",
                # 🔥 ลด Temperature ลงเหลือ 0.7 (ให้มันนิ่งขึ้น ไม่ฟุ้งซ่านเกินไป)
                temperature=0.7, 
                max_tokens=1024,
            )
            return {"result": chat_completion.choices[0].message.content}
        
    except Exception as e:
        return {"result": f"Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)