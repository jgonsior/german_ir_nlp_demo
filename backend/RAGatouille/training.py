from ragatouille import RAGTrainer
import pandas as pd
import os
import shutil
from pathlib import Path
import argparse
import random 
import csv

def highest_alphabetical_directory(current_path):
    directories = [d for d in os.listdir(current_path) if os.path.isdir(os.path.join(current_path, d))]
    
    if not directories:
        return None

    highest_directory = max(directories)
    return highest_directory

def most_recent_created_path(base_path):
    current_path = base_path
    for i in range(3):
        current_path = os.path.join(current_path, highest_alphabetical_directory(current_path))
    
    return current_path

def move_content(source_path, destination_path):
    # Check if source path exists
    if not os.path.exists(source_path):
        print(f"Source path '{source_path}' does not exist.")
        return
    
    # Check if destination path exists, create it if it doesn't
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    
    # Iterate through each item in the source path
    for item in os.listdir(source_path):
        # Create full paths for items in source and destination
        source_item_path = os.path.join(source_path, item)
        destination_item_path = os.path.join(destination_path, item)
        
        # If it's a file, move it to the destination
        if os.path.isfile(source_item_path):
            shutil.move(source_item_path, destination_item_path)
            print(f"Moved file '{item}' to '{destination_path}'.")
        # If it's a directory, recursively call move_content
        elif os.path.isdir(source_item_path):
            move_content(source_item_path, destination_item_path)
    
    # After moving all content, remove the source directory
    os.rmdir(source_path)
    print(f"Removed source directory '{source_path}'.")

def split_list(lst, n):
    # Calculate the size of each chunk
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

def main(args):
    train_data = f"{args.union_train_data}-{args.num_negatives}neg"

    corpus = pd.read_csv(args.corpus_path).values.tolist()

    triples = pd.read_json(args.triples_path, lines=True)[["question", "positive_contexts", "negative_contexts"]].values.tolist()
    if args.num_negatives < len(triples[0][2]):
        triples = [[q, p, random.sample(n, args.num_negatives)] for q, p, n in triples]
    triple_parts = split_list(triples, args.num_parts)
    for e in args.epochs:
        for part in range(1, args.num_parts+1):
            if (part == 1 or part == "1"):
                if (e == 1 or e == "1"):
                    pretrained_model_name_or_path = args.pretrained_model_name_or_path
                else:
                    pretrained_model_name_or_path = f"backend/data/colbert/checkpoints/{args.base_model_name}/{train_data}/epoch{int(e)-1}/part{args.num_parts}"
            else:
                pretrained_model_name_or_path = f"backend/data/colbert/checkpoints/{args.base_model_name}/{train_data}/epoch{int(e)}/part{part-1}"

            trainer = RAGTrainer(model_name = f"{args.base_model_name}-{train_data}",
                    pretrained_model_name = pretrained_model_name_or_path,
                    language_code="de")

            # This step handles all the data processing. Check whether data has already been preprocessed
            colbert_training_data_path = f"backend/data/colbert/training_data/{train_data}/epoch{e}/part{part}"
            trainer.prepare_training_data(raw_data=triple_parts[part-1],
                                            all_documents = corpus,
                                            data_out_path=colbert_training_data_path, 
                                            num_new_negatives = 0, 
                                            mine_hard_negatives=False)

            model_output_path = trainer.train(
                    batch_size=16,
                    nbits=4, # How many bits will the trained model use when compressing indexes
                    maxsteps=10_000_000, # Maximum steps hard stop
                    use_ib_negatives=True, # Use in-batch negative to calculate loss
                    dim=128, # How many dimensions per embedding. 128 is the default and works well.
                    learning_rate=5e-6, # Learning rate, small values ([3e-6,3e-5] work best if the base model is BERT-like, 5e-6 is often the sweet spot)
                    doc_maxlen=512, # Maximum document length. Because of how ColBERT works, smaller chunks (128-256) work very well.
                    use_relu=False, # Disable ReLU -- doesn't improve performance
                    warmup_steps="auto", # Defaults to 10%
                    )
            
            # original colbert code forgot to propagate model_output_path -> hence we have to find it our selves

            move_content(os.path.join(most_recent_created_path(".ragatouille/colbert/none"), "checkpoints/colbert"),
                            f"backend/data/colbert/checkpoints/{args.base_model_name}/{train_data}/epoch{e}/part{part}")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--base_model_name', type=str, default="bert-base-german-cased", help="BERT backbone")
    parser.add_argument('--pretrained_model_name_or_path', type=str, help="e.g. 'bert-base-german-cased' or 'backend/data/colbert/checkpoints/bert-base-german-cased/GermanDPR/epoch1'")
    parser.add_argument('--union_train_data', type=str, help="e.g. 'GermanDPR-XQA' when training a model already trained on GermanDPR additionally on XQA")
    parser.add_argument('--triples_path', type=str, help="e.g. 'backend/data/qa/GermanDPR/train_triples.jsonl'")
    parser.add_argument('--corpus_path', type=str, help="e.g. 'backend/data/qa/GermanDPR/train_passages.csv' (according to triples)")
    parser.add_argument("--epochs", metavar="N", type=str, nargs="+",
                        help="List of integers separated by spaces")
    parser.add_argument('--num_negatives', type=int, default=1, help="how many negative contexts of the training triples should be used")
    parser.add_argument('--num_parts', type=int, default=1, help="in how many parts of equal size should the training triples be split")
    
    args = parser.parse_args()

    main(args)

    # example call: conda run -n RAG_env_conda --no-capture-output python3 backend/RAGatouille/training.py --pretrained_model_name_or_path backend/data/colbert/checkpoints/bert-base-german-cased/GermanDPR/epoch1 --base_model_name bert-base-german-cased --union_train_data GermanDPR-XQA --triples_path backend/data/qa/XQA/train_triples.jsonl --corpus_path backend/data/qa/XQA/train_passages.csv --epochs 2
