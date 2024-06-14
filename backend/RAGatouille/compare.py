from ragatouille import RAGPretrainedModel
import pandas as pd
import torch
import json
import os
import shutil 
import argparse
from tqdm import tqdm

def overwrite_index_metadata(json_file_path):
    # Load the JSON data from the file
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    # Check if the keys exist in the dictionary
    if "config" in data and "index_name" in data["config"]:
        # Overwrite the value associated with index_name under config
        data["config"]["index_name"] = data["config"]["index_name"].split("/")[-1]

        # Save the modified dictionary back to the JSON file
        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print("Value overwritten successfully.")
    else:
        print("Key 'config' or 'index_name' not found in the dictionary.")

def main(args):
    qa_pairs = pd.read_json(args.triples_path, lines=True)[["question", "positive_contexts", "positive_context_ids"]].values.tolist()
    num_qa_pairs = len(qa_pairs)
    queries = [qa[0] for qa in qa_pairs]
    answer_ids = [qa[2] for qa in qa_pairs]
    print("args.models", args.models)
    print("num qa pairs:", num_qa_pairs, flush=True)
    statistics = {pretrained_model_path.split("/")[-2]:{f"recall@{k}":0 for k in Ks} for pretrained_model_path in args.models.split(" ")}

    for pretrained_model_path in args.models.split(" "):
        print("pretrained_model_path", pretrained_model_path)
        #index_path = f"backend/data/colbert/indexes/{args.base_model_name}/{args.train_data}/epoch{e}/part{part}"
        index_path = f".ragatouille/test/{pretrained_model_path}"
        #pretrained_model_path = f"backend/data/colbert/checkpoints/{args.base_model_name}/{args.train_data}/epoch{e}/part{part}"
        print("CUDA available: ", torch.cuda.is_available(), flush = True)
        passages_df = pd.read_csv(args.corpus_path, header=None)
        passage_ids = passages_df[0].tolist()
        passages = passages_df[1].tolist()

        print("index_path: ", index_path, flush = True)
        print("model_path: ", pretrained_model_path, flush=True)
        RAG = RAGPretrainedModel.from_pretrained(pretrained_model_path)

        print("...start indexing", flush = True)
        RAG.index(
                collection=passages, 
                document_ids=passage_ids,
                #document_metadatas=[{"entity": "person", "source": "wikipedia"}],

                index_name=index_path, 
                max_document_length=512,
                split_documents=False,
                bsize=32
        )
        #overwrite_index_metadata(f"{index_path}/metadata.json")




        results = RAG.search(query=queries, k=max(Ks))

        for i in tqdm(range(num_qa_pairs), desc=f"calculating recall for {pretrained_model_path}"):
                #answer = answers[i].replace("\n", "\\n")
                retrieved_passage_ids = [x["document_id"] for x in results[i]]
                for k in Ks:
                        if any([id in retrieved_passage_ids[:k] for id in answer_ids[i]]):
                                statistics[pretrained_model_path.split("/")[-2]][f"recall@{k}"] += 1/num_qa_pairs

        print(statistics)
        new_data = statistics
        old_data = {}
        if os.path.exists(args.statistics_path): 
              df_old = pd.read_csv(args.statistics_path, index_col=0).transpose()
              old_data = df_old.to_dict()
        old_data.update(new_data)
        df_new = pd.DataFrame(old_data)
        df_new.transpose().to_csv(args.statistics_path)



Ks = [1,2,3,4,5,6,8,10,20,50,100]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--models", metavar="N", type=str, nargs="+", default = "backend/data/colbert/best/GermanDPR-XQA-HP-10neg-DPRe1p8-XQAe1p18-HPe1p15/checkpoint backend/data/colbert/best/GermanDPR-XQA-HP-10neg-DPRe1p7-XQAe1p18-HPe1p19/checkpoint backend/data/colbert/best/old/checkpoint",
                        help="List of integers separated by spaces")
    
    parser.add_argument('--corpus_path', type=str, default="backend/data/qa/HP/passages.csv", help="e.g. 'backend/data/qa/HP/passages.csv' (according to triples)")

    parser.add_argument('--triples_path', type=str, default="backend/data/qa/HP/test_triples.jsonl", help="e.g. 'backend/data/qa/HP/test_triples.jsonl'")

    parser.add_argument('--statistics_path', type=str, default="backend/data/statistics/statistics_comparison.csv", help="")

    args = parser.parse_args()

    main(args)
