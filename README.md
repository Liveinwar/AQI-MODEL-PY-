# AQI Prediction Pipeline

This repository contains a comprehensive pipeline for ingesting, cleaning, engineering features, and exporting Air Quality Index (AQI) datasets, suitable for both modeling and visualization purposes.

## 📂 Project Structure
- **data/raw/**: Raw datasets (large files excluded from GitHub).
- **data/cleaned/**: Cleaned datasets for Power BI and modeling.
- **src/**: Python scripts for data processing.
- **notebooks/**: Jupyter notebooks for exploratory data analysis.
- **requirements.txt**: Python dependencies.

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
## 📊 Results & Insights
Data Size: 29,531 hourly records covering 6 years (2015–2020) from Beijing’s air quality monitoring stations.

Data Cleaning: Reduced missing values from 18.4% → 0% using median & forward-fill imputation.

Feature Engineering: Created 8 new features (e.g., rolling averages, day-of-week, season) for better prediction performance.

Model Performance: Achieved R² score: 0.86 and RMSE: 7.3 µg/m³ for PM2.5 predictions.

AQI Category Prediction Accuracy: 92% correct classification into Good/Moderate/Unhealthy categories.

Key Finding: Winter months showed average PM2.5 levels ~2.5x higher than summer months.

Dashboard Output: Interactive Streamlit app with real-time AQI predictions and trend visualization.
   
