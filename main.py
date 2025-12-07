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



# --- Config Keys with Fallback ---
# รองรับหลาย API Keys สำหรับ Fallback
GROQ_API_KEYS = []

# โหลด API Keys ทั้งหมด (GROQ_API_KEY, GROQ_API_KEY_2, GROQ_API_KEY_3, ...)
primary_key = os.environ.get("GROQ_API_KEY")
if primary_key:
    GROQ_API_KEYS.append(primary_key)

backup_key = os.environ.get("GROQ_API_KEY_2")
if backup_key:
    GROQ_API_KEYS.append(backup_key)

# สร้าง clients สำหรับแต่ละ key
groq_clients = [Groq(api_key=key) for key in GROQ_API_KEYS]

def get_groq_client(index=0):
    """ดึง Groq client ตาม index"""
    if index < len(groq_clients):
        return groq_clients[index]
    return None

print(f"🔑 Loaded {len(GROQ_API_KEYS)} Groq API Key(s)")

AI_SYSTEM_PROMPT = """
คุณคือ 'Best Bot' เพื่อน AI ที่ชิลล์และเป็นกันเอง 😎

สไตล์การตอบ:
- พูดแบบเพื่อนสนิท สบายๆ เหมือนคุยกัน
- ตอบสั้นๆ กระชับ ไม่ยาวเกินไป
- ใส่ emoji บ้างเป็นบางครั้ง (ไม่ต้องเยอะมาก)
- ถ้าถามง่ายๆ ตอบสั้นๆ ถ้าถามยาก ค่อยอธิบายละเอียด
- ให้กำลังใจและเชียร์เสมอ

กฎสำคัญ:
1. ห้ามใช้ดาวจุด ** เน้นข้อความ
2. ถ้ามีหลายข้อ ให้ขึ้นบรรทัดใหม่แต่ละข้อ (แต่ไม่ต้องเว้นบรรทัดว่าง)
3. ตัวอย่างการเขียนรายการ:

1. ข้อแรก
2. ข้อสอง  
3. ข้อสาม

4. พูดแบบธรรมชาติ ไม่ต้องเป็นทางการ
5. ใส่ emoji ได้แต่พอดี (2-3 ตัวต่อข้อความ)

ตัวอย่างที่ดี:
"โอเค! ให้ช่วยนะ 😊

ทำแบบนี้:
1. เปิดไฟล์ที่ต้องการ
2. แก้โค้ดตรงที่ต้องการ
3. บันทึกแล้วลองรัน

ง่ายๆแค่นี้เอง ลองดูนะ!"

ห้ามตอบแบบนี้:
"คุณต้องทำแบบนี้ 1. เปิดไฟล์ 2. แก้โค้ด 3. บันทึก" ❌ (รวมกันเป็นบรรทัดเดียว)
"คุณต้องทำ **แบบนี้** นะ **สำคัญมาก**" ❌ (ใช้ดาวจุดเยอะ)
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
    
    # จับตัวเลข 1. 2. 3. ที่ไม่ได้อยู่ต้นบรรทัดอยู่แล้ว และใส่ newline ด้านหน้า
    # (?<!\n) = ต้องไม่มี newline อยู่ด้านหน้า (negative lookbehind)
    # (\d+\.) = ตัวเลขตามด้วยจุด เช่น 1. 2. 3.
    text = re.sub(r'(?<!\n)(\s*)(\d+\.)\s+', r'\n\2 ', text)  # ใช้ \n เดียว ไม่ use \n\n
    
    # ล้างบรรทัดว่างซ้ำซ้อน (เกิน 2 บรรทัด)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

@app.get("/")
@app.head("/")
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

@app.get("/gg.png")
async def serve_logo():
    """Serve logo file"""
    # Try dist/ first (production)
    if os.path.exists("dist/gg.png"):
        return FileResponse("dist/gg.png")
    # Fallback to public/ (development)
    elif os.path.exists("public/gg.png"):
        return FileResponse("public/gg.png")
    else:
        return {"error": "Logo not found"}

@app.post("/calculate")
async def calculate_logic(request: QueryRequest):
    """
    ระบบ Fallback: ลอง API Key แรกก่อน ถ้าโดน rate limit จะสลับไป Key ถัดไป
    """
    if not groq_clients:
        return {"result": "Error: ไม่พบ Groq API Key"}
    
    last_error = None
    
    # ลอง API Keys ทีละตัว
    for key_index, client in enumerate(groq_clients):
        try:
            # 📸 Vision - ใช้ Groq Llama 3.2 Vision
            if request.image:
                prompt_text = request.prompt if request.prompt else "รูปนี้คืออะไร"
                full_prompt = f"{AI_SYSTEM_PROMPT}\n\nโจทย์รูปภาพ: {prompt_text}"
                
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": full_prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": request.image
                                    }
                                }
                            ]
                        }
                    ],
                    model="meta-llama/llama-4-scout-17b-16e-instruct",  # Llama 4 Vision (แทน llama-3.2-90b ที่ถูกยกเลิก)
                    temperature=0.7,
                    max_tokens=1024,
                )
                print(f"✅ Vision สำเร็จด้วย Key #{key_index + 1}")
                return {"result": format_response(chat_completion.choices[0].message.content)}
            
            # 📝 Text - ใช้ Groq Llama 3.3
            else:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": AI_SYSTEM_PROMPT},
                        {"role": "user", "content": request.prompt}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                    max_tokens=1024,
                )
                print(f"✅ Text สำเร็จด้วย Key #{key_index + 1}")
                return {"result": format_response(chat_completion.choices[0].message.content)}
        
        except Exception as e:
            last_error = str(e)
            # ถ้าเป็น rate limit error ให้ลอง key ถัดไป
            if "rate" in last_error.lower() or "limit" in last_error.lower() or "429" in last_error:
                print(f"⚠️ Key #{key_index + 1} โดน rate limit, สลับไป Key ถัดไป...")
                continue
            else:
                # ถ้าเป็น error อื่น ให้ return ทันที
                return {"result": f"Error: {last_error}"}
    
    # ถ้าลองทุก key แล้วยังไม่ได้
    return {"result": f"❌ API Keys ทั้งหมดโดน rate limit กรุณารอสักครู่แล้วลองใหม่"}

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