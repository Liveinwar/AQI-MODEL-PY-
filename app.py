# app.py (run: streamlit run app.py)

import streamlit as st
import pandas as pd
from config import CLEAN_DIR

# Load the cleaned hourly AQI data from the pipeline
df = pd.read_csv(CLEAN_DIR / "aqi_cleaned_hourly.csv", parse_dates=['timestamp'])

# Set timestamp as index for time-series operations
df = df.set_index('timestamp')

# Dropdown selector for station ID
station = st.selectbox("Station", df['station_id'].unique())

# Filter data for that station
sub = df[df['station_id'] == station]

# Daily average PM2.5 line chart
st.line_chart(sub['pm25'].resample('D').mean())

# Show the latest 50 records in a table
st.write(sub.tail(50))

