import json
import pandas as pd
import random

TRAINING_DATA_PATH_GERMAN_DPR = "data/qa/GermanDPR/GermanDPR_train.json"
TEST_DATA_PATH_GERMAN_DPR = "data/qa/GermanDPR/GermanDPR_test.json"

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

def create_GermanDPR_train_files(training_data_path, triple_path, passages_path):
    triples, passages = get_raw_data_GermanDPR(training_data_path)
    df_t = pd.DataFrame(triples, columns=["question", "positive_contexts", "negative_contexts"])
    df_t.to_json(triple_path, orient="records", lines=True)
    print(pd.read_json(triple_path, lines = True))
    passages_df = pd.DataFrame(list(set(passages)))
    passages_df.to_csv(passages_path, index=False, header=False)

def create_GermanDPR_test_qa_file(test_data_path, qa_path):
    qa_pairs = []
    with open(test_data_path, "r", encoding="utf-8") as test_file:
        data = json.load(test_file)

    for q in data:
        positive_ctxs = q["positive_ctxs"][0]["text"].replace('\n', '\\n')
        qa_pairs.append([q["question"], positive_ctxs])
    
    df_qa_pairs = pd.DataFrame(qa_pairs, columns=["question", "answer"])
    df_qa_pairs.to_json(qa_path, orient="records", lines=True)
    print(pd.read_json(qa_path, lines = True))
    
def create_full_passage_corpus(passages_path, full_corpus_output_path):
    _, train_corpus = get_raw_data_GermanDPR(TRAINING_DATA_PATH_GERMAN_DPR)
    _, test_corpus = get_raw_data_GermanDPR(TEST_DATA_PATH_GERMAN_DPR)
    passages_df = pd.read_csv(passages_path, header=None)
    passages = list(set(passages_df[1].tolist() + train_corpus + test_corpus))

    passages_df = pd.DataFrame(passages)
    passages_df.to_csv(full_corpus_output_path, index=False, header=False)

if __name__ == "__main__":
    # creates triples for training (q, [p+], [p-,p-,p-]) in json format
    create_GermanDPR_train_files(TRAINING_DATA_PATH_GERMAN_DPR, 
            "data/qa/GermanDPR/train_triples.jsonl",
            "data/qa/GermanDPR/train_passages.csv")

    # creates the qa pairs for testing (evaluation)
    create_GermanDPR_test_qa_file(TEST_DATA_PATH_GERMAN_DPR, 
            "data/qa/GermanDPR/test_qa_pairs.jsonl") 

    # creates the full passage corpus which is used for evaluation/retrieval (has to be indexed) 
    #create_full_passage_corpus(OLD_PASSAGES_PATH, OLD_FULL_CORPUS_PATH)
    #create_full_passage_corpus(NEW_PASSAGES_PATH, NEW_FULL_CORPUS_PATH)
    