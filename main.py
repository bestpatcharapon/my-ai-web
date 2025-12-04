import os
import io
import base64
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from groq import Groq
import google.generativeai as genai
from PIL import Image
import uvicorn

app = FastAPI()

# Add CORS middleware - allowing both dev and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you might want to restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (React build)
if os.path.exists("dist"):
    app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")



# --- Config Keys ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
vision_model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        vision_model = genai.GenerativeModel('gemini-2.0-flash') # หรือ 2.0-flash
    except: pass

AI_SYSTEM_PROMPT = """
คุณคือ 'Best Bot' เพื่อน AI ที่ฉลาดและเป็นกันเอง 🤖

สไตล์การตอบ:
- พูดแบบเพื่อน สบายๆ ไม่เป็นทางการจนเกินไป
- ตอบตรงประเด็น กระชับ ได้ใจความ
- ถ้าเรื่องไหนยาก อธิบายง่ายๆ ให้เข้าใจ
- ให้กำลังใจผู้ใช้ ถ้าเห็นว่าเขาดูเครียด

กฎสำคัญที่ต้องปฏิบัติเสมอ:
1. ห้ามใช้ดาวจุด ** หรือสัญลักษณ์พิเศษเยอะๆ
2. ต้องขึ้นบรรทัดใหม่ (newline) หลังแต่ละข้อเสมอ
3. ถ้ามีหลายข้อ ให้เขียนแบบนี้:

1. ข้อแรก (ขึ้นบรรทัดใหม่)
2. ข้อสอง (ขึ้นบรรทัดใหม่)
3. ข้อสาม (ขึ้นบรรทัดใหม่)

4. ใส่อิโมจิได้แค่นิดหน่อยเท่านั้น (ไม่เกิน 2-3 ตัวต่อข้อความ)
5. พูดแบบธรรมชาติ ไม่ต้องเน้นหลายๆ คำด้วยการใส่ดาวจุด

ตัวอย่างการตอบที่ถูกต้อง (สังเกตว่าแต่ละข้อขึ้นบรรทัดใหม่):
"เข้าใจเลยครับ! คุณต้องทำแบบนี้นะ

ขั้นตอนง่ายๆ:

1. เปิดไฟล์ที่ต้องการ
2. แก้ไขโค้ดในส่วนที่เกี่ยวข้อง
3. บันทึกแล้วลองรันดู

ลองทำตามนี้ดูนะครับ ถ้ามีปัญหาบอกได้เลย 😊"

ห้ามตอบแบบนี้ (ข้อความรวมกันไม่ขึ้นบรรทัดใหม่):
"คุณต้องทำแบบนี้นะ 1. เปิดไฟล์ 2. แก้ไขโค้ด 3. บันทึก" ❌

ห้ามตอบแบบนี้ (ใช้ดาวจุดเยอะ):
"คุณต้องทำ **แบบนี้** นะ **สำคัญมาก** ⭐✨🎯" ❌
"""

class QueryRequest(BaseModel):
    prompt: str
    image: Optional[str] = None

def format_response(text: str) -> str:
    """
    ปรับแต่งข้อความให้อ่านง่ายขึ้น:
    - บังคับให้ขึ้นบรรทัดใหม่หลัง numbered list (1. 2. 3.)
    """
    import re
    
    # แทนที่ " 1. " ด้วย "\n\n1. " (เว้นว่างด้านหน้า)
    # แต่ไม่แทนที่ถ้าอยู่ต้นบรรทัดอยู่แล้ว
    text = re.sub(r'(?<!\n) (\d+)\. ', r'\n\1. ', text)
    
    # ล้างบรรทัดว่างซ้ำซ้อน (เกิน 2 บรรทัด)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

@app.get("/")
async def serve_frontend():
    """Serve React production build or development fallback"""
    # Production: serve from dist/
    if os.path.exists("dist/index.html"):
        with open("dist/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    # Development fallback
    elif os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    else:
        return HTMLResponse(
            content="<h1>AI Chatbot Backend Running</h1><p>Frontend not built. Run: npm run build</p>",
            status_code=200
        )

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
                return {"result": format_response(response.text)}
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
            return {"result": format_response(chat_completion.choices[0].message.content)}
        
    except Exception as e:
        return {"result": f"Error: {str(e)}"}

if __name__ == "__main__":
    # Startup logging
    print("=" * 50)
    print("Starting AI Chatbot Server...")
    print(f"  - dist/index.html exists: {os.path.exists('dist/index.html')}")
    print(f"  - index.html exists: {os.path.exists('index.html')}")
    if os.path.exists("dist"):
        print(f"  - dist/ contents: {os.listdir('dist')}")
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=10000)