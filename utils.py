# utils.py
import pandas as pd
import numpy as np
from typing import Iterable

def safe_parse_datetime(df: pd.DataFrame, date_cols: Iterable[str]=None, date_col: str=None):
    """
    Robustly create a 'timestamp' column from either:
     - a single ISO 'date'/'datetime' column, or
     - separate year, month, day, hour columns (common in PRSA dataset).
    """
    if date_col and date_col in df.columns:
        ts = pd.to_datetime(df[date_col], errors="coerce")
        return ts
    # try year/month/day/hour
    if set(["year","month","day","hour"]).issubset(df.columns):
        ts = pd.to_datetime(df[['year','month','day','hour']].rename(columns={'hour':'hour'}), errors='coerce')
        return ts
    # fallback try index or guess
    # try to find column containing 'date' substring:
    for c in df.columns:
        if "date" in c.lower() or "time" in c.lower():
            try:
                return pd.to_datetime(df[c], errors="coerce")
            except Exception:
                pass
    raise ValueError("No parsable date columns found.")

def numeric_cols(df: pd.DataFrame):
    return df.select_dtypes(include=[np.number]).columns.tolist()
