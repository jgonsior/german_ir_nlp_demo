#!/usr/bin/env python3

import json

def load_passages():
    ps = []
    with open("witcher-passages.tsv", "r") as f:
        for line in f.readlines()[1:]:
            ps.append(line.split("\t")[1])

    return ps

def make_corpus(passages):
    with open("corpus.jsonl", "w") as f:
        for idx, p in enumerate(passages):
            passage_as_dict = {
                    "_id": str(idx),
                    "title": "",
                    "text": p
            }
            f.write(json.dumps(passage_as_dict) + "\n")

def main():
    ps = load_passages()[:50]
    make_corpus(ps)

if __name__ == "__main__":
    main()
