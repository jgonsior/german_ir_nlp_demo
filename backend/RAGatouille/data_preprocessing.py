import json
import pandas as pd
import random

TRAINING_DATA_PATHS_GERMAN_DPR = ["backend/data/qa/GermanDPR/GermanDPR_train.json", 
                                  "backend/data/qa/GermanDPR/GermanDPR_test.json"]
TEST_DATA_PATH_GERMAN_DPR = "backend/data/qa/GermanDPR/GermanDPR_test.json"

TRAINING_DATA_PATHS_XQA = ["backend/data/qa/XQA/dev_doc.json", 
                           "backend/data/qa/XQA/test_doc.json"]
TEST_DATA_PATH_XQA = "backend/data/qa/XQA/test_doc.json"

FULL_CORPUS_PATH = "backend/data/wiki_dumps/harry_potter_corpus.csv"
WIKI_DUMP_PATH = "backend/data/wiki_dumps/harry_potter.json"

def get_raw_data_GermanDPR(data_path):
    '''
    used format tiples: list of triplets of list of strings [([q_string], [p_string], [n1_string, n2_string, n3_string]), ... ]
    used format corpus: list of strings
    '''
    with open(data_path, "r", encoding="utf-8") as train_file:
        data = json.load(train_file)
    
    triples = []
    corpus = []

    for q in data:
        query = q["question"]
        positive_ctxs = [passage["text"].replace('\n', '\\n') for passage in q["positive_ctxs"]]

        hard_negative_ctxs = [passage["text"].replace('\n', '\\n') for passage in q["hard_negative_ctxs"]]
        triples.append([query, positive_ctxs,hard_negative_ctxs])
        corpus += positive_ctxs
        corpus += hard_negative_ctxs

    return triples, corpus

def create_GermanDPR_train_files(training_data_paths, triple_path, passages_path):
    triples = []
    passages = []

    for training_data_path in training_data_paths:
        t, p = get_raw_data_GermanDPR(training_data_path)
        triples += t
        passages += p
    df_t = pd.DataFrame(triples, columns=["question", "positive_contexts", "negative_contexts"])
    df_t.to_json(triple_path, orient="records", lines=True)
    print(pd.read_json(triple_path, lines = True))
    passages = list(set(passages))
    passages_df = pd.DataFrame({"passage_id": range(0, len(passages)), "passage": passages})
    passages_df.to_csv(passages_path, index=False, header=False)

def create_QXA_train_files(training_data_paths, triple_path, passages_path):
    wiki_dump_passages = {}
    with open("backend/data/qa/XQA/dump/wiki_text.json") as wiki_dump_file:
        for line in wiki_dump_file:
            data = json.loads(line)
            wiki_dump_passages[data["id"]] = data["document"]

    triples = []
    passages = {}
    for training_data_path in training_data_paths:
        with open(training_data_path, 'r') as file:
            for line in file:
                data = json.loads(line)
                question = data[0]["question"].replace("<Query>", "Wer oder Was")
                positive_contexts = []
                negative_contexts = []
                for answer in data:
                    positive_contexts.append(answer["document"])
                    passages["XQA-" + answer["document_id"]] = answer["document"].replace("\n","\\n")

                for key in random.sample(wiki_dump_passages.keys(), 10):
                    negative_contexts.append(wiki_dump_passages[key])
                    passages["XQA-dump-" + key] = wiki_dump_passages[key].replace("\n","\\n")
                triples.append([question, positive_contexts, negative_contexts])
    
    df_t = pd.DataFrame(triples, columns=["question", "positive_contexts", "negative_contexts"])
    df_t.to_json(triple_path, orient="records", lines=True)
    print(pd.read_json(triple_path, lines = True))
    passages_df = pd.DataFrame(list(passages.items()), columns=["passage_id", "passage"])
    passages_df.to_csv(passages_path, index=False, header=False)   

def create_full_passage_corpus_from_wiki_dump(wiki_dump_path, full_corpus_output_path):
    num_passages = 0
    with open(wiki_dump_path, 'r') as file:
        wiki_dump_data = json.load(file)
    df = pd.DataFrame(columns=['id', 'passage'])
    for wiki in wiki_dump_data:
        id = wiki["id"]
        if(id == 18535):
            break
        title = wiki["title"]
        for i, passage in enumerate(wiki["text"]):
            new_row = {"id": f"{id}-{i}", "passage": f"[{title}] {passage}"}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            num_passages += 1
    print("num passages: ", num_passages)
    df.to_csv(full_corpus_output_path, index=False)

def convert_corpus_jsonl_to_csv(corpus_jsonl_path, output_path):
    corpus_df = pd.read_json(corpus_jsonl_path, lines=True)
    corpus_df['text'] = corpus_df['title'] + ' ' + corpus_df['text']
    corpus_df.drop(columns=['title'], inplace=True)
    corpus_df.to_csv(output_path, index=False, header=False)

def main():
    # creates triples for training (q, [p+], [p-,p-,p-]) in json format
    create_GermanDPR_train_files(TRAINING_DATA_PATHS_GERMAN_DPR, 
            "backend/data/qa/GermanDPR/train_triples.jsonl",
            "backend/data/qa/GermanDPR/train_passages.csv")
    create_QXA_train_files(TRAINING_DATA_PATHS_XQA, 
            "backend/data/qa/XQA/train_triples.jsonl",
            "backend/data/qa/XQA/train_passages.csv"
    )

    # creates a csv file of harry passage from the wiki dump 
    # old: create_full_passage_corpus_from_wiki_dump(WIKI_DUMP_PATH, FULL_CORPUS_PATH)
    convert_corpus_jsonl_to_csv("backend/data/wiki_dumps/corpus.jsonl", "backend/data/qa/HP/passages.csv")
  
if __name__ == "__main__":
    main()
    
