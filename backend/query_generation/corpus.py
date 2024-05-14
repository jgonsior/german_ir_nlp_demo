import os
import json

def create_corpus():

    id = 1
    corpus = []
    with open('backend/query_generation/hp-gpl/harry_potter_unicode_processed.json', 'r') as file:
        data = json.load(file)
        for wikipage in data:
            for paragraph in wikipage['text']:
                doc = {}
                doc['id'] = id
                doc['title'] = wikipage['title']
                doc['text'] = paragraph
                id += 1
                corpus.append(doc)

    with open('backend/query_generation/hp-gpl/corpus.json', 'w', encoding='utf-8') as file:
        json.dump(corpus, file, indent=1, ensure_ascii=False)

if __name__ == "__main__":
    create_corpus()
