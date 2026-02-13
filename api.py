
"""
AI SUPPORT SYSTEM - REST API
Description: FastAPI-based web service that provides endpoints for ticket submission. 
             It validates customer data using Pydantic, triggers the AI analysis, 
             and coordinates the database storage process.
Endpoints: 
    - GET /: Health check
    - POST /analyze-ticket: Core processing endpoint
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from database import DatabaseManager
from ai_engine import SupportAI

app = FastAPI(title="AI Support API")
db = DatabaseManager()
ai = SupportAI()

# Müşteriden gelecek verinin yapısını tanımlıyoruz
class SupportRequest(BaseModel):
    full_name: str
    email: EmailStr
    message: str

@app.get("/")
def home():
    return {"status": "AI Support System is Online"}

@app.post("/analyze-ticket")
def analyze_ticket(request: SupportRequest):
    try:
        # 1. Kullanıcıyı bul veya e-postasına göre yeni oluştur
        # (DatabaseManager içine eklediğimiz get_or_create_user fonksiyonunu kullanıyoruz)
        user_id = db.get_or_create_user(request.full_name, request.email)
        
        # 2. Mesajı AI ile analiz et
        analysis = ai.analyze_message(request.message)
        
        # 3. Analizi ve bilet bilgilerini veritabanına kaydet
        db.save_ticket(user_id=user_id, message=request.message, analysis=analysis)
        
        return {
            "message": "Ticket processed successfully!",
            "user_id": user_id,
            "ai_analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))