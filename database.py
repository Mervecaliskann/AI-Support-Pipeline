"""
AI SUPPORT SYSTEM - DATABASE MANAGEMENT
Description: Handles all PostgreSQL operations using SQLAlchemy. Manages the 
             relational link between customers (users) and support tickets, 
             ensuring data integrity through Foreign Key constraints.
Design Pattern: Manager class for centralized database operations.
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        # .env dosyasındaki DB_URL ile bağlantı kurar
        self.engine = create_engine(os.getenv("DB_URL"))

    def get_or_create_user(self, full_name, email):
        """Kullanıcıyı e-postasına göre arar, yoksa yeni oluşturur."""
        check_query = text("SELECT user_id FROM users WHERE email = :email")
        
        with self.engine.connect() as conn:
            result = conn.execute(check_query, {"email": email}).fetchone()
            
            if result:
                # Kullanıcı zaten varsa, mevcut ID'yi dön
                return result[0]
            
            # Kullanıcı yoksa, yeni bir tane oluştur ve otomatik ID'sini al
            insert_query = text("""
                INSERT INTO users (full_name, email) 
                VALUES (:name, :email) RETURNING user_id
            """)
            new_user = conn.execute(insert_query, {"name": full_name, "email": email}).fetchone()
            conn.commit()
            return new_user[0]

    def save_ticket(self, user_id, message, analysis):
        """AI analiz sonuçlarını bilet tablosuna kaydeder."""
        query = text("""
            INSERT INTO support_tickets (user_id, message_text, category, sentiment, priority)
            VALUES (:u_id, :msg, :cat, :sent, :prio)
        """)
        
        with self.engine.connect() as conn:
            conn.execute(query, {
                "u_id": user_id,
                "msg": message,
                "cat": analysis.get("category"),
                "sent": analysis.get("sentiment"),
                "prio": analysis.get("priority")
            })
            conn.commit()
        print("✅ Veritabanına başarıyla kaydedildi!")