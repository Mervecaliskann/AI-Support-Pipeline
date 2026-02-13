"""
AI SUPPORT SYSTEM - CLI TESTING MODULE
Description: A legacy CLI-based module used for initial prototyping and 
             unit testing of the AI and Database integration logic. 
             Now replaced by the production-ready FastAPI (api.py).
"""

from database import DatabaseManager
from ai_engine import SupportAI

def run_app():
    db = DatabaseManager()
    ai = SupportAI()

    print("🚀 AI Support System Aktif!")
    user_msg = input("Müşteri mesajını girin: ")

    # 1. AI ile analiz et
    print("🤖 AI analiz ediyor...")
    analysis = ai.analyze_message(user_msg)
    print(f"Analiz Sonucu: {analysis}")

    # 2. Veritabanına kaydet (Örnek olarak user_id: 1 veriyoruz)
    db.save_ticket(user_id=1, message=user_msg, analysis=analysis)

if __name__ == "__main__":
    run_app()