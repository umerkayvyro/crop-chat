import os
import json
from collections import defaultdict

EXCLUDED_DISTRICTS = {"Punjab", "Sindh"}
FOLDER = "shared_docs"

def extract_year_and_district(filename):
    """Extract year and district from the filename."""
    base = os.path.basename(filename)
    year_match = None
    district = None

    if "Jan-Apr_2025_" in base:
        year_match = 2025
        district = base.split("Jan-Apr_2025_")[-1].replace(".json", "").replace("_", " ").strip()
    elif "Jun-Dec_2024_" in base:
        year_match = 2024
        district = base.split("Jun-Dec_2024_")[-1].replace(".json", "").replace("_", " ").strip()
    
    return year_match, district

def load_agricultural_land_data(folder_path):
    agri_land_by_year = {
        2024: defaultdict(float),
        2025: defaultdict(float),
    }

    for filename in os.listdir(folder_path):
        if filename.endswith(".json") and ("Jan-Apr_2025_" in filename or "Jun-Dec_2024_" in filename):
            year, district = extract_year_and_district(filename)
            if not year or not district or district in EXCLUDED_DISTRICTS:
                continue
            try:
                with open(os.path.join(folder_path, filename), 'r') as file:
                    data = json.load(file)
                    crop_data = data.get("cropTypeData", {})
                    total_agri = sum(crop_data.get(crop, 0.0) for crop in ["Wheat", "Cotton", "Others"])
                    agri_land_by_year[year][district] += total_agri
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    return agri_land_by_year

def print_top_districts(agri_data, year):
    print(f"\nTop 10 districts by agricultural land in {year} (Wheat + Cotton + Others):")
    sorted_data = sorted(agri_data.items(), key=lambda x: x[1], reverse=True)[:10]
    for i, (district, acres) in enumerate(sorted_data, start=1):
        print(f"{i}. {district}: {acres:.2f} acres")

if __name__ == "__main__":
    agri_land_by_year = load_agricultural_land_data(FOLDER)

    for year in [2024, 2025]:
        print_top_districts(agri_land_by_year[year], year)
