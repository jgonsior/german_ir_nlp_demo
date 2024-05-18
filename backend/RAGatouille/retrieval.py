from ragatouille import RAGPretrainedModel
import torch
BASE_MODEL_NAME = "bert-base-german-cased"
TRAINING_DATA_NAME = "GermanDPR-XQA-HP"
EPOCH = 1
INDEX_PATH = f"backend/data/colbert/indexes/{BASE_MODEL_NAME}/{TRAINING_DATA_NAME}/epoch{EPOCH}"

if __name__ == "__main__":

    k = 5
    RAG = RAGPretrainedModel.from_index(INDEX_PATH)
    results = RAG.search(query="Wer hat Snape umgebracht?", k=k)
    print(results)


    # get embeddings. not sure what this 1-dimensional vector is
    embeddings = torch.load("backend/data/colbert/indexes/bert-base-german-cased/GermanDPR-XQA-HP/epoch1/0.codes.pt")
    print(embeddings[0])
    print(embeddings.shape)