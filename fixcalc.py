import os
import json

def divide_numbers_by_2(obj):
    if isinstance(obj, dict):
        return {k: divide_numbers_by_2(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [divide_numbers_by_2(item) for item in obj]
    elif isinstance(obj, (int, float)):
        return obj / 2
    else:
        return obj

# Set this to your target directory
directory = '/Users/vyromacbook/Desktop/langchain-agent/cricket-chatbot/shared_docs'

for filename in os.listdir(directory):
    if filename.endswith('.json'):
        file_path = os.path.join(directory, filename)

        # Read JSON
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Process and overwrite
        updated_data = divide_numbers_by_2(data)

        with open(file_path, 'w') as f:
            json.dump(updated_data, f, indent=2)

print("All JSON files processed and overwritten.")
