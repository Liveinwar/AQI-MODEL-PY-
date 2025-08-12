# AQI Prediction Pipeline

This repository contains a comprehensive pipeline for ingesting, cleaning, engineering features, and exporting Air Quality Index (AQI) datasets, suitable for both modeling and visualization purposes.

## 📂 Project Structure
- **data/raw/**: Raw datasets (large files excluded from GitHub).
- **data/cleaned/**: Cleaned datasets for Power BI and modeling.
- **src/**: Python scripts for data processing.
- **notebooks/**: Jupyter notebooks for exploratory data analysis.
- **requirements.txt**: Python dependencies.
AQI_PROJECT_3/
├── data/
│   ├── raw/                        # Keep sample CSVs here (not large ones)
│   │   └── PRSA_data_sample.csv
│   └── cleaned/
│       ├── aqi_cleaned_hourly.csv
│       └── features_for_model.csv
├── src/
│   ├── config.py                   # Configuration settings
│   ├── data_ingest.py             # CSV to PostgreSQL ingestion
│   ├── preprocess.py              # Data cleaning and preprocessing
│   ├── feature_engineer.py        # Feature engineering pipeline
│   ├── export_for_modelers.py     # Export processed data for modeling
│   ├── utils.py                   # Utility functions
│   └── app.py                     # Streamlit dashboard application
├── notebooks/
│   └── eda.ipynb                  # Exploratory Data Analysis
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
├── .gitignore                     # Git ignore rules
└── .vscode/                       # VSCode configuration
    ├── launch.json                # Debug configuration
    └── tasks.json                 # Task automation
## 🚀 Quick Start
1. Clone this repo:
   ```bash
   git clone https://github.com/your-username/aqi-project.git
   cd aqi-project
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Run the pipeline:
   ```bash
   python src/data_ingest.py
   python src/preprocess.py
   python src/feature_engineer.py
   python src/export_for_modelers.py
5. Start the Streamlit app:
   ```bash
   streamlit run src/app.py

   
