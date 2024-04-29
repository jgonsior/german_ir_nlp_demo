from ragatouille import RAGTrainer
import pandas as pd
import os
import shutil
from pathlib import Path

BASE_MODEL_NAME = "bert-base-german-cased"
TRAINING_DATA_NAME = "GermanDPR"
TRIPLES_PATH = "backend/data/qa/GermanDPR/train_triples.jsonl" 
CORPUS_PATH = "backend/data/qa/GermanDPR/train_passages.csv" 
EPOCHS = [1,2] # training has to start with epoch 1. this variable currently only states how many epochs are trained

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

if __name__ == "__main__":
    corpus = pd.read_csv(CORPUS_PATH).values.tolist()
    trained_model_from_previous_epoch = None

    triples = pd.read_json(TRIPLES_PATH, lines=True).values.tolist()
    MODEL_NAME = f"{BASE_MODEL_NAME}-{TRAINING_DATA_NAME}"
    for e in EPOCHS:
        if e == EPOCHS[0]:
            pretrained_model_name_or_path = BASE_MODEL_NAME
        else:
            pretrained_model_name_or_path = trained_model_from_previous_epoch

        trainer = RAGTrainer(model_name = MODEL_NAME,
                pretrained_model_name = pretrained_model_name_or_path,
                language_code="de")

        # This step handles all the data processing. Check whether data has already been preprocessed
        colbert_training_data_path = f"data/colbert/training_data/{TRAINING_DATA_NAME}"
        if not os.path.exists(colbert_training_data_path) or not any(os.listdir(colbert_training_data_path)):
            trainer.prepare_training_data(raw_data=triples,
                                            all_documents = corpus,
                                            data_out_path=colbert_training_data_path, 
                                            num_new_negatives = 0, 
                                            mine_hard_negatives=False)
        else:
            trainer.data_dir = Path(colbert_training_data_path)

        model_output_path = trainer.train(
                batch_size=32,
                nbits=4, # How many bits will the trained model use when compressing indexes
                maxsteps=500000, # Maximum steps hard stop
                use_ib_negatives=True, # Use in-batch negative to calculate loss
                dim=128, # How many dimensions per embedding. 128 is the default and works well.
                learning_rate=5e-6, # Learning rate, small values ([3e-6,3e-5] work best if the base model is BERT-like, 5e-6 is often the sweet spot)
                doc_maxlen=512, # Maximum document length. Because of how ColBERT works, smaller chunks (128-256) work very well.
                use_relu=False, # Disable ReLU -- doesn't improve performance
                warmup_steps="auto", # Defaults to 10%
                )
        
        # original colbert code forgot to propagate model_output_path -> hence we have to find it our selves
        trained_model_from_previous_epoch = f"data/colbert/checkpoints/{BASE_MODEL_NAME}/{TRAINING_DATA_NAME}/epoch{str(e)}"
        move_content(os.path.join(most_recent_created_path(".ragatouille/colbert/none"), "checkpoints/colbert"),
                        trained_model_from_previous_epoch)