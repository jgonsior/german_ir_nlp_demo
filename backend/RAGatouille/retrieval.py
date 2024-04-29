from ragatouille import RAGPretrainedModel
import torch
BASE_MODEL_NAME = "bert-base-german-cased"
TRAINING_DATA_NAME = "GermanDPR"
EPOCH = 1
FULL_CORPUS_NAME = "harry_potter_corpus"
INDEX_PATH = f"backend/data/colbert/indexes/{BASE_MODEL_NAME}/{TRAINING_DATA_NAME}/{FULL_CORPUS_NAME}/epoch{EPOCH}"

if __name__ == "__main__":

    k = 1
    results = RAG.search(query="Wie Heißt die Eule von Harry Potter?", k=k)
    print(results)
    # embeddings = torch.load("data/colbert/indexes/bert-base-german-cased/GermanDPR/harry_potter_corpus/epoch1/0.codes.pt")

    # print(embeddings.shape)