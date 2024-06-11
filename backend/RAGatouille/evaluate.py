import json
from ragatouille import RAGPretrainedModel
import pandas as pd
from tqdm import tqdm
import os 
import argparse

def main(args):
    qa_pairs = pd.read_json(args.triples_path, lines=True)[["question", "positive_contexts", "positive_context_ids"]].values.tolist()
    num_qa_pairs = len(qa_pairs)
    print("num qa pairs:", num_qa_pairs, flush=True)
    
    statistics = {f"{args.base_model_name}-{args.train_data}-epoch{e}-part{part}":{f"recall@{k}":0 for k in Ks} for e in args.epochs for part in range(1,args.num_parts+1)}
    best_checkpoint_path = ""
    best_checkpoint_quality = -1
    for e in args.epochs:
        for part in range(1,args.num_parts+1):
            index_path = f"backend/data/colbert/indexes/{args.base_model_name}/{args.train_data}/epoch{e}/part{part}"
            RAG = RAGPretrainedModel.from_index(index_path)

            queries = [qa[0] for qa in qa_pairs]
            #answers = [qa[1] for qa in qa_pairs]
            answer_ids = [qa[2] for qa in qa_pairs]

            results = RAG.search(query=queries, k=max(Ks))

            for i in tqdm(range(num_qa_pairs), desc=f"calculating recall for epoch{e} and part{part}"):
                #answer = answers[i].replace("\n", "\\n")
                retrieved_passage_ids = [x["document_id"] for x in results[i]]
                for k in Ks:
                    if any([id in retrieved_passage_ids[:k] for id in answer_ids[i]]):
                        statistics[f"{args.base_model_name}-{args.train_data}-epoch{e}-part{part}"][f"recall@{k}"] += 1/num_qa_pairs

            # find best checkpoint
            quality_of_new_checkpoint = statistics[f"{args.base_model_name}-{args.train_data}-epoch{e}-part{part}"][f"recall@5"]
            if quality_of_new_checkpoint > best_checkpoint_quality:
                best_checkpoint_path = f"backend/data/colbert/checkpoints/{args.base_model_name}/{args.train_data}/epoch{e}/part{part}"
                best_checkpoint_quality = quality_of_new_checkpoint

            print(statistics)
            new_data = statistics
            old_data = {}
            if os.path.exists(args.statistics_path): 
                df_old = pd.read_csv(args.statistics_path, index_col=0).transpose()
                old_data = df_old.to_dict()
            old_data.update(new_data)
            df_new = pd.DataFrame(old_data)
            df_new.transpose().to_csv(args.statistics_path)

    # pass best checkpoint path to next train script
    print(best_checkpoint_path)

Ks = [1,2,3,4,5,6,8,10,20,50,100]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--base_model_name', type=str, default="bert-base-german-cased", help="e.g. 'bert-base-german-cased'")
    parser.add_argument('--train_data', type=str, help="e.g. 'GermanDPR-XQA-HP'")
    parser.add_argument('--triples_path', type=str, help="e.g. 'backend/data/qa/HP/eval_triples.jsonl'")
    #parser.add_argument('--epochs', type=int, help="number of epochs to eval")
    parser.add_argument("--epochs", metavar="N", type=str, nargs="+",
                        help="List of integers separated by spaces")
    parser.add_argument("--num_parts", type=int, help="")
    parser.add_argument('--statistics_path', type=str, default="backend/data/statistics/statistics.csv", help="e.g. 'backend/data/statistics/statistics.csv'")

    args = parser.parse_args()

    main(args)
