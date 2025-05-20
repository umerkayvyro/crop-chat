import os
import json
import re
from collections import defaultdict

# Set of districts to exclude (can expand as needed)
EXCLUDED_DISTRICTS = {"Punjab", "Sindh"}

def extract_district_name(filename, pattern_prefix):
    """
    Extracts the district name from a filename using the prefix pattern like 'Jun-Dec_2024_'
    """
    base = os.path.basename(filename)
    if pattern_prefix in base:
        district_part = base.split(pattern_prefix, 1)[-1]
        district_name = district_part.replace(".json", "").replace("_", " ").strip()
        return district_name
    return None

def load_crop_data(folder_path, crop_name, pattern_in_filename):
    crop_data = defaultdict(float)
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".json") and pattern_in_filename in filename:
            district = extract_district_name(filename, pattern_in_filename)
            if not district or district in EXCLUDED_DISTRICTS:
                continue
            try:
                with open(os.path.join(folder_path, filename), 'r') as file:
                    data = json.load(file)
                    crop_value = data.get("cropTypeData", {}).get(crop_name, 0.0)
                    crop_data[district] += crop_value
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    return crop_data

def print_top_10(crop_data, crop_name):
    print(f"\nTop 10 districts for {crop_name} (in acres, excluding Punjab & Sindh):")
    sorted_data = sorted(crop_data.items(), key=lambda x: x[1], reverse=True)[:10]
    for i, (district, acres) in enumerate(sorted_data, start=1):
        print(f"{i}. {district}: {acres:.2f} acres")

if __name__ == "__main__":
    folder = "shared_docs"

    # Load only correctly tagged files
    wheat_data = load_crop_data(folder, "Wheat", "Jan-Apr_2025_")
    cotton_data = load_crop_data(folder, "Cotton", "Jun-Dec_2024_")

    print_top_10(wheat_data, "Wheat")
    print_top_10(cotton_data, "Cotton")
