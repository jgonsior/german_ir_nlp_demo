import json

from tools import format_json


def create_corpus():
    """
    create corpus.jsonl for gpl query generation from preprocessed wiki
    """
    corpus = []
    with open('backend/query_generation_tommy/hp-ger/harry_potter_unicode_processed.json', 'r') as file:
        data = json.load(file)
        for wikipage in data:
            page_id = wikipage["id"]
            paragraph_id = 0
            for paragraph in wikipage["text"]:
                doc = {}
                doc["_id"] = f"{page_id}-{paragraph_id}"
                doc["title"] = wikipage["title"]
                doc["text"] = paragraph
                paragraph_id += 1
                corpus.append(doc)

    with open('backend/query_generation_tommy/hp-ger/corpus.jsonl', 'w', encoding='utf-8') as file:
        for obj in corpus:
            json.dump(obj, file, ensure_ascii=False)
            file.write("\n")


if __name__ == "__main__":
    create_corpus()

    # After the top is executed once:
    format_json.jsonl_to_json("backend/query_generation/hp-gpl/corpus.jsonl")
    # python -m query_generation.corpus
