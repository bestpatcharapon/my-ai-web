# 🤖 Best Chat Bot

AI Chatbot สุดเจ๋งที่ใช้เทคโนโลยี **Llama 3.3 70B** ผ่าน Groq API พร้อมอินเตอร์เฟซที่สวยงาม รองรับภาษาไทยเต็มรูปแบบ!

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-FF6B00?style=for-the-badge&logo=groove&logoColor=white)

## ✨ ฟีเจอร์เด็ด

- 💬 **ตอบคำถามภาษาไทยได้อย่างลื่นไหล** - ขับเคลื่อนด้วย Llama 3.3 70B
- 🎨 **UI สวยงาม Dark Mode** - ออกแบบสไตล์ ChatGPT
- ⚡ **เร็วแรง** - ใช้ Groq API ที่มี inference speed สูงสุด
- 📱 **Responsive Design** - ใช้งานได้ทั้งมือถือและคอมพิวเตอร์
- 🔄 **Real-time Chat** - แสดงผลแบบ real-time พร้อม loading animation

## 🚀 การติดตั้งและใช้งาน

### 1. Clone โปรเจกต์

```bash
git clone https://github.com/bestpatcharapon/my-ai-web.git
cd my-ai-web
```

### 2. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 3. ตั้งค่า API Key

สร้าง Environment Variable สำหรับ Groq API Key:

```bash
export GROQ_API_KEY="your-groq-api-key-here"
```

> 💡 **วิธีหา API Key:** สมัครฟรีได้ที่ [console.groq.com](https://console.groq.com)

### 4. รันโปรเจกต์

```bash
python main.py
```

เปิดเว็บเบราว์เซอร์ที่: **http://localhost:10000**

## 📦 โครงสร้างโปรเจกต์

```
my-ai-web/
├── index.html         # Frontend UI (HTML + CSS + JS)
├── main.py           # Backend API (FastAPI)
├── requirements.txt  # Python dependencies
└── README.md         # คู่มือการใช้งาน
```

## 🛠️ เทคโนโลยีที่ใช้

- **Backend**: FastAPI + Uvicorn
- **AI Model**: Llama 3.3 70B Versatile (via Groq)
- **Frontend**: HTML5 + CSS3 + Vanilla JavaScript
- **Markdown**: Marked.js สำหรับแสดงผล Markdown
- **Icons**: Font Awesome 6

## 🌐 Deploy ไปยัง Render

### ขั้นตอนการ Deploy:

1. Push โค้ดไปยัง GitHub
2. สร้าง Web Service ใหม่ที่ [Render](https://render.com)
3. เชื่อมต่อกับ GitHub repository
4. ตั้งค่า Environment Variable:
   - Key: `GROQ_API_KEY`
   - Value: `your-groq-api-key`
5. Deploy! 🚀

### คำสั่ง Build (Render):

```bash
pip install -r requirements.txt
```

### คำสั่ง Start (Render):

```bash
python main.py
```

## 💡 วิธีใช้งาน

1. เปิดเว็บไซต์
2. พิมพ์คำถามหรือข้อความในช่องพิมพ์ข้อความ
3. กด Enter หรือคลิกปุ่มส่ง ✈️
4. รอ AI ตอบกลับมา
5. สนุกกับการสนทนา! 🎉

## 🎯 ตัวอย่างการใช้งาน

```
👤 User: "อธิบาย Quantum Computing ให้ฟังหน่อย"
🤖 AI: "Quantum Computing คือ..."

👤 User: "เขียนโค้ด Python สำหรับ Fibonacci"
🤖 AI: "แน่นอนครับ นี่คือตัวอย่างโค้ด..."
```

## 📝 License

MIT License - ใช้งานได้อย่างอิสระตามที่ต้องการ

## 👨‍💻 ผู้พัฒนา

**Best Patcharapon**

- GitHub: [@bestpatcharapon](https://github.com/bestpatcharapon)

## 🙏 Credits

- [Groq](https://groq.com) - ให้บริการ AI inference ความเร็วสูง
- [Meta](https://ai.meta.com) - พัฒนา Llama Models
- [FastAPI](https://fastapi.tiangolo.com) - Web framework ที่เร็วและใช้งานง่าย

---

⭐ ถ้าชอบโปรเจกต์นี้ อย่าลืมกด Star ด้วยนะครับ!
