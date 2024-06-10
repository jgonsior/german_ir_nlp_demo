import json


def remove_invisible_chars(text: str) -> str:

    invisible_chars = dict.fromkeys(map(ord, "\u200B\u200C\u200D\u00AD\u2028\u2029\u00a0\u2014"), None)
    invisible_chars[ord("\u2028")] = ord(" ")
    invisible_chars[ord("\u2029")] = ord(" ")
    invisible_chars[ord("\u00a0")] = ord(" ")
    invisible_chars[ord("\u2014")] = ""
    return text.translate(invisible_chars)


def process_files(unprocessed_file: str, path_for_output: str):
    try:
        # Read the JSON file
        with open(unprocessed_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Process and clean data
        if isinstance(data, dict) and "text" in data:
            data["text"] = [remove_invisible_chars(line) for line in data["text"]]
        elif isinstance(data, list):
            for item in data:
                if "text" in item:
                    item["text"] = [remove_invisible_chars(line) for line in item["text"]]

        # Write the cleaned data
        with open(path_for_output, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    except json.JSONDecodeError as e:
        print(f"JSON error occurred in {unprocessed_file}: {e}")
    except FileNotFoundError:
        print(f"File not found: {unprocessed_file}")
    except Exception as e:
        print(f"An error occurred while processing {unprocessed_file}: {e}")


def main(unprocessed_file: str, path_for_output: str):
    process_files(unprocessed_file, path_for_output)


if __name__ == "__main__":
    main(
        unprocessed_file="backend/preprocessing/data/harry_potter_processed.json",
        path_for_output="backend/preprocessing/data/harry_potter_unicode_processed.json",
    )
