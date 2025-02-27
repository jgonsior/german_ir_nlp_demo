import json
import format_json


def create_corpus(dir: str):
    """    
    create corpus.jsonl for gpl query generation from preprocessed wiki json

    Arguments:
        dir -- target directory, where corpus.jsonl should be written at
    """
    corpus = []
    with open('../../preprocessing/data/harry_potter_unicode_processed.json', 'r') as file:
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

    with open(f'{dir}/corpus.jsonl', 'w', encoding='utf-8') as file:
        for obj in corpus:
            json.dump(obj, file, ensure_ascii=False)
            file.write("\n")


if __name__ == "__main__":
    dir = "hp-ger"
    create_corpus(dir)

    # create corpus.json file from .jsonl for inverted_index script
    #format_json.jsonl_to_json(f"{dir}/corpus.jsonl")