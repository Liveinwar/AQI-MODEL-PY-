# config.py - central config (edit DB creds + paths)
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
CLEAN_DIR = DATA_DIR / "cleaned"

CSV_PATH = RAW_DIR / "PRSA_data_2010.1.1-2014.12.31.csv"

# PostgreSQL connection string (SQLAlchemy)
DB_USER = "postgres"
DB_PASS = "8617"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "aqi_db"
DB_CONN = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
