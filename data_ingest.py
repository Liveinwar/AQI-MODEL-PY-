'''# data_ingest.py
"""
Ingest a CSV into PostgreSQL in chunks. Handles two modes:
- direct CSV import (local file)
- load-from-URL (if direct raw CSV URL)
"""
import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm
from config import CSV_PATH, DB_CONN
from utils import safe_parse_datetime

CHUNK = 20000

def ingest_csv_to_postgres(csv_path=CSV_PATH, table_name="raw_aqi"):
    engine = create_engine(DB_CONN, echo=False)
    # read in chunks
    for chunk in tqdm(pd.read_csv(csv_path, chunksize=CHUNK, low_memory=False), desc="ingesting"):
        # parse timestamp robustly
        try:
            chunk['timestamp'] = safe_parse_datetime(chunk, date_col='date')
        except Exception:
            try:
                chunk['timestamp'] = safe_parse_datetime(chunk)
            except Exception as e:
                print("Date parsing failed:", e)
                raise
        # drop rows where timestamp couldn't be parsed
        chunk = chunk.dropna(subset=['timestamp'])
        # normalize column names
        chunk.columns = [c.strip().lower() for c in chunk.columns]
        # keep core columns or everything: rename known columns
        # example: pm25 may be named 'pm2.5' in Beijing dataset
        if 'pm2.5' in chunk.columns:
            chunk = chunk.rename(columns={'pm2.5':'pm25'})
        # write to_sql (append)
        chunk.to_sql(table_name, engine, if_exists='append', index=False)

    print("Ingestion complete.")

if __name__ == "__main__":
    ingest_csv_to_postgres()
'''
# data_ingest.py
"""
Ingest a CSV into PostgreSQL in chunks. Handles two modes:
- direct CSV import (local file)
- load-from-URL (if direct raw CSV URL)
"""
import pandas as pd
from sqlalchemy import create_engine, inspect
from tqdm import tqdm
from config import CSV_PATH, DB_CONN
from utils import safe_parse_datetime

CHUNK = 20000

def ingest_csv_to_postgres(csv_path=CSV_PATH, table_name="raw_aqi"):
    engine = create_engine(DB_CONN, echo=False)
    
    # Get the actual table columns from the database
    inspector = inspect(engine)
    if inspector.has_table(table_name):
        db_columns = set(col['name'] for col in inspector.get_columns(table_name))
        print(f"Database table columns: {db_columns}")
    else:
        db_columns = None
        print(f"Table '{table_name}' does not exist yet.")
    
    # read in chunks
    for chunk in tqdm(pd.read_csv(csv_path, chunksize=CHUNK, low_memory=False), desc="ingesting"):
        # parse timestamp robustly
        try:
            chunk['timestamp'] = safe_parse_datetime(chunk, date_col='date')
        except Exception:
            try:
                chunk['timestamp'] = safe_parse_datetime(chunk)
            except Exception as e:
                print("Date parsing failed:", e)
                raise
        
        # drop rows where timestamp couldn't be parsed
        chunk = chunk.dropna(subset=['timestamp'])
        
        # normalize column names
        chunk.columns = [c.strip().lower() for c in chunk.columns]
        
        # keep core columns or everything: rename known columns
        # example: pm25 may be named 'pm2.5' in Beijing dataset
        if 'pm2.5' in chunk.columns:
            chunk = chunk.rename(columns={'pm2.5':'pm25'})
        
        # Filter columns to match database schema if table exists
        if db_columns is not None:
            # Keep only columns that exist in the database
            csv_columns = set(chunk.columns)
            columns_to_keep = csv_columns.intersection(db_columns)
            columns_to_drop = csv_columns - db_columns
            
            if columns_to_drop:
                print(f"Dropping columns not in database: {columns_to_drop}")
                chunk = chunk[list(columns_to_keep)]
        
        # write to_sql (append)
        chunk.to_sql(table_name, engine, if_exists='append', index=False)

    print("Ingestion complete.")

if __name__ == "__main__":
    ingest_csv_to_postgres()