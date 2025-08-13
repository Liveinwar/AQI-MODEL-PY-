# feature_engineer.py
"""
Create model-ready features (rolling means, lags, cyclical encodings).
Save a CSV that the model team can pick up.
"""
import pandas as pd
import numpy as np
from config import CLEAN_DIR, DB_CONN
from sqlalchemy import create_engine

def create_features(df: pd.DataFrame):
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    df = df.set_index('timestamp').sort_index()
    # identify pollutant columns
    pm_cols = [c for c in df.columns if 'pm25' in c or 'pm10' in c]
    # create rolling windows for pm25 if present
    if 'pm25' in df.columns:
        df['pm25_roll3'] = df['pm25'].rolling(window=3, min_periods=1).mean()
        df['pm25_roll6'] = df['pm25'].rolling(window=6, min_periods=1).mean()
        df['pm25_roll24'] = df['pm25'].rolling(window=24, min_periods=1).mean()
        df['pm25_lag1'] = df['pm25'].shift(1)
        df['pm25_lag24'] = df['pm25'].shift(24)
    if 'pm10' in df.columns:
        df['pm10_roll24'] = df['pm10'].rolling(24, min_periods=1).mean()
        df['pm10_lag1'] = df['pm10'].shift(1)
    # cyclical encoding of hour & day-of-week
    df['hour'] = df.index.hour
    df['dow']  = df.index.dayofweek
    df['hour_sin'] = np.sin(2*np.pi*df['hour']/24)
    df['hour_cos'] = np.cos(2*np.pi*df['hour']/24)
    df['dow_sin']  = np.sin(2*np.pi*df['dow']/7)
    df['dow_cos']  = np.cos(2*np.pi*df['dow']/7)
    # drop rows with NaN after shifting (first 24 rows)
    df = df.dropna(subset=['pm25_lag24'] if 'pm25_lag24' in df.columns else [])
    return df.reset_index()

def main():
    engine = create_engine(DB_CONN)
    df = pd.read_sql_table('aqi_cleaned', engine)
    feats = create_features(df)
    out = CLEAN_DIR / "features_for_model.csv"
    feats.to_csv(out, index=False)
    feats.to_sql('aqi_features', engine, if_exists='replace', index=False)
    print("Features written to:", out)

if __name__ == "__main__":
    main()
