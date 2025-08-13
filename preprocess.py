# preprocess.py
"""
Load raw table (or CSV), do cleaning, missing-value imputation, resampling and save cleaned CSV & DB table.
"""
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from config import DB_CONN, CSV_PATH, CLEAN_DIR
from utils import safe_parse_datetime, numeric_cols
CLEAN_DIR.mkdir(parents=True, exist_ok=True)

def load_raw(csv_path=CSV_PATH):
    df = pd.read_csv(csv_path, low_memory=False)
    df.columns = [c.strip().lower() for c in df.columns]
    # unify pm2.5 col name
    if 'pm2.5' in df.columns:
        df = df.rename(columns={'pm2.5':'pm25'})
    df['timestamp'] = safe_parse_datetime(df, date_col='date') if 'date' in df.columns else safe_parse_datetime(df)
    df = df.dropna(subset=['timestamp']).sort_values('timestamp').reset_index(drop=True)
    return df

def impute_timeseries(df: pd.DataFrame, group_col='station_id'):
    """
    - set timestamp index
    - resample to hourly (if not already hourly)
    - forward-fill for small gaps (<3 hours)
    - median impute for longer gaps
    """
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    # if station_id not present, create single group
    if 'station_id' not in df.columns:
        df['station_id'] = 'site_0'
    out_frames = []
    for station, g in df.groupby('station_id'):
        g = g.set_index('timestamp').sort_index()
        # resample hourly (common)
        g = g.resample('H').asfreq()
        numeric = numeric_cols(g)
        # small-gap ffill for numeric
        g[numeric] = g[numeric].ffill(limit=3)
        # for remaining NaNs, use median of the entire series for that column
        for col in numeric:
            if g[col].isna().any():
                med = g[col].median(skipna=True)
                g[col] = g[col].fillna(med)
        # backfill non-numeric if needed
        out = g.reset_index()
        out['station_id'] = station
        out_frames.append(out)
    res = pd.concat(out_frames, axis=0).sort_values(['station_id','timestamp']).reset_index(drop=True)
    return res

def run_and_save():
    df = load_raw()
    print("Raw shape:", df.shape)
    cleaned = impute_timeseries(df)
    print("Cleaned shape:", cleaned.shape)
    out_csv = CLEAN_DIR / "aqi_cleaned_hourly.csv"
    cleaned.to_csv(out_csv, index=False)
    # optional: write to postgres
    engine = create_engine(DB_CONN)
    cleaned.to_sql('aqi_cleaned', engine, if_exists='replace', index=False)
    print("Saved cleaned CSV ->", out_csv)
    return cleaned

if __name__ == "__main__":
    run_and_save()
