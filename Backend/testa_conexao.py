from database import SessionLocal
from sqlalchemy import text

try:
    db = SessionLocal()
    db.execute(text("SELECT 1"))  # Testa uma query simples
    print("✅ Conexão com o banco de dados funcionando!")
except Exception as e:
    print("❌ Erro ao conectar com o banco:")
    print(e)
finally:
    db.close()