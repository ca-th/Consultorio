# Backend/test_db.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DB = os.getenv("MYSQL_DB")

# --- Print statements para depuração ---
print(f"DEBUG DB: User={MYSQL_USER}, Host={MYSQL_HOST}, DB={MYSQL_DB}")
if MYSQL_PASSWORD:
    print("DEBUG DB: Password loaded (not displayed for security)")
else:
    print("DEBUG DB: Password NOT loaded!")
print(f"DEBUG DB: PATH={os.getcwd()}") # Adiciona este para ver o diretório atual
print(f"DEBUG DB: ENV_FILE_EXISTS={os.path.exists('.env')}") # Verifica se o .env existe
# ----------------------------------------

DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"

print(f"DEBUG DB: DATABASE_URL={DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL)
    print("DEBUG DB: Engine created successfully!")
    # Tenta uma conexão simples para verificar
    with engine.connect() as connection:
        result = connection.execute("SELECT 1").scalar()
        print(f"DEBUG DB: DB connection test result: {result}")
except Exception as e:
    print(f"ERROR: Failed to create engine or connect: {e}")
    # É crucial ver esta mensagem de erro.
    # Não levante a exceção aqui para ver todos os prints
    # raise # Remova o raise temporariamente
    engine = None # Define engine como None se falhar para evitar NameError mais tarde neste script
# ----------------------------------------------------------

if engine: # Só define se o engine foi criado com sucesso
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    print("DEBUG DB: SessionLocal and Base defined.")
else:
    print("DEBUG DB: Engine was not created. SessionLocal and Base not defined.")