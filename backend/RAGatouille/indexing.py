from ragatouille import RAGPretrainedModel
import pandas as pd
import torch
import json
import os
import shutil 

BASE_MODEL_NAME = "bert-base-german-cased"
TRAINING_DATA_NAME = "GermanDPR"
EPOCH = 1
PRETRAINED_MODEL_PATH = f"data/colbert/checkpoints/{BASE_MODEL_NAME}/{TRAINING_DATA_NAME}/epoch{EPOCH}"

FULL_CORPUS_NAME = "harry_potter_corpus"
FULL_CORPUS_PATH = f"data/wiki_dumps/{FULL_CORPUS_NAME}.csv"
INDEX_PATH = f"data/colbert/indexes/{BASE_MODEL_NAME}/{TRAINING_DATA_NAME}/{FULL_CORPUS_NAME}/epoch{EPOCH}"

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

if __name__ == "__main__":
    print("CUDA available: ", torch.cuda.is_available(), flush = True)
    passages_df = pd.read_csv(FULL_CORPUS_PATH, header=None)
    passage_ids = passages_df[0].tolist()
    passages = passages_df[1].tolist()

    print("index_path: ", INDEX_PATH, flush = True)
    
    RAG = RAGPretrainedModel.from_pretrained(PRETRAINED_MODEL_PATH)

    print("...start indexing", flush = True)
    RAG.index(
        collection=passages, 
        document_ids=passage_ids,
        #document_metadatas=[{"entity": "person", "source": "wikipedia"}],
        index_name=INDEX_PATH, 
        max_document_length=512,
        split_documents=False,
        bsize=32
    )
    move_content(f".ragatouille/colbert/indexes/{INDEX_PATH}", INDEX_PATH)
    overwrite_index_metadata(f"{INDEX_PATH}/metadata.json")

    
