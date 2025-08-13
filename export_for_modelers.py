# export_for_modelers.py
"""
Provide artifact(s) for modelers:
- features CSV
- a small JSON manifest describing columns and preprocessing steps
"""
import json
from pathlib import Path
from config import CLEAN_DIR

def write_manifest(path: Path):
    manifest = {
        "features_csv": str(path / "features_for_model.csv"),
        "preprocessing": {
            "resample": "hourly",
            "ffill_limit_hours": 3,
            "median_impute": True,
            "cyclical_encodings": ["hour", "day_of_week"]
        },
        "notes": "pm25 was renamed from pm2.5 where needed. Nulls handled by ffill and median."
    }
    with open(path / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    print("manifest saved:", path / "manifest.json")

if __name__ == "__main__":
    write_manifest(Path(__file__).resolve().parents[1] / "data" / "cleaned")
