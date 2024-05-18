from ragatouille import RAGPretrainedModel
import pandas as pd
import torch
import json
import os
import shutil 
import argparse

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

def main(args):
    for e in args.epochs:
        index_path = f"backend/data/colbert/indexes/{args.base_model_name}/{args.train_data}/epoch{e}"
        pretrained_model_path = f"backend/data/colbert/checkpoints/{args.base_model_name}/{args.train_data}/epoch{e}"
        print("CUDA available: ", torch.cuda.is_available(), flush = True)
        passages_df = pd.read_csv(args.corpus_path, header=None)
        passage_ids = passages_df[0].tolist()
        passages = passages_df[1].tolist()

        print("index_path: ", index_path, flush = True)
        
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
        move_content(f".ragatouille/colbert/indexes/{index_path}", index_path)
        overwrite_index_metadata(f"{index_path}/metadata.json")

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--base_model_name', type=str, default="bert-base-german-cased", help="e.g. 'bert-base-german-cased'")
    parser.add_argument('--train_data', type=str, help="e.g. 'GermanDPR-XQA-HP'")
    parser.add_argument('--corpus_path', type=str, default="backend/data/qa/HP/passages.csv", help="e.g. 'backend/data/qa/HP/passages.csv' (according to triples)")
    parser.add_argument("--epochs", metavar="N", type=str, nargs="+",
                        help="List of integers separated by spaces")
    args = parser.parse_args()

    main(args)