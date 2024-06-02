import json
from collections import defaultdict
from typing import DefaultDict, Dict, List


def load_data(file_path: str):
    """Loads a `.json` file that contains the data for the Harry Potter articles that will be presented,
        which uses the name `inv_index_wissenschaftskommunikation_normalized.json` with the structure:
        {
            "<Article Heading>": {
                "<token>" : ["DOC_ID-PASSAGE_ID", ...],
                ...
            },
        }

        Example:
        --------------

        {
            "Harry Potter": {
                "harry": ["119-0", "119-2"], where 119 represents DOC_ID and 0, 2 represents PASSAGE_ID
            }
        }

    Args:
        file_path (str): Path to where the `inv_index_wissenschaftskommunikation_normalized.json` file is stored.

    Returns:
        json: Loaded `inv_index_wissenschaftskommunikation_normalized.json` file for processing.
    """

    with open(file_path, "r") as file:
        return json.load(file)


def summarize_data(data: json):
    """Summarises the list of entries for every <token>, in case a <token> appears in multiple <Article Headings>.

    Args:
        data (json): The loaded data from `load_data()`

    Returns:
        DefaultDict[List]: The summarised data
    """
    summarised_results = defaultdict(list)
    for _, entries in data.items():
        for key, values in entries.items():
            summarised_results[key].extend(values)
    return summarised_results


def sort_and_save(summarised_results):
    """Takes the list of entries ["DOC_ID-PASSAGE_ID", ..] for every <token> and transforms the "PASSAGE_ID" into an integer that will be used for sorting.

    Args:
        summarised_results (DefaultDict[List]):

    Returns:
        Dict: A dictionary in which every
    """
    for word, entries in summarised_results.items():
        unsorted_results = [entry.split("-") for entry in entries]
        for item in unsorted_results:
            item[-1] = int(item[-1])

        sorted_results = sorted(unsorted_results, key=lambda x: x[-1])
        transformed_data = [f"{item[0]}-{item[-1]}" for item in sorted_results]
        summarised_results[word] = transformed_data

    with open("backend/inv_index/inv_index_wisschenschaftskommunikation_normalized_summarised.json", "w", encoding="utf-8") as output:
        json.dump(summarised_results, output, indent=4, sort_keys=True, ensure_ascii=False)


def main():
    data = load_data("backend/inv_index/inv_index_wissenschaftskommunikation_normalized.json")
    summarised_results = summarize_data(data)
    sort_and_save(summarised_results)


if __name__ == "__main__":
    main()
