import json

UNPROCESSED_FILE = "backend/preprocessing/data/harry_potter.json"

# Reading the JSON file
with open(UNPROCESSED_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

with open("backend/preprocessing/data/harry_potter_unicode_processed.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)


def remove_invisible_chars(text):
    # Dictionary of invisible Unicode characters to replace
    replacements = {
        "\u200B": "",  # Zero-width space
        "\u200C": "",  # Zero-width non-joiner
        "\u200D": "",  # Zero-width joiner
        "\u00AD": "",  # Soft hyphen
        "\u2028": " ",  # Line separator
        "\u2029": " ",  # Paragraph separator
        "\u00a0": " ",
    }
    # Replace each character using the dictionary
    for char, repl in replacements.items():
        text = text.replace(char, repl)
    return text


PROCESSED_FILE = "backend/preprocessing/data/harry_potter_unicode_processed.json"
output_path = "backend/preprocessing/data/harry_potter_unicode_processed.json"

try:
    with open(PROCESSED_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Assuming the text to clean is in a specific field
    if isinstance(data, dict) and "text" in data:
        data["text"] = [remove_invisible_chars(line) for line in data["text"]]
    elif isinstance(data, list):
        for item in data:
            if "text" in item:
                item["text"] = [remove_invisible_chars(line) for line in item["text"]]

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

except Exception as e:
    print(f"An error occurred: {e}")
