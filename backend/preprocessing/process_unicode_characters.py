import json

file_path = "backend/preprocessing/data/harry_potter.json"

# Reading the JSON file
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

with open("backend/preprocessing/data/harry_potter_unicode_processed.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
