import pandas as pd
from ragatouille import RAGPretrainedModel
BASE_MODEL_NAME = "bert-base-german-cased"
TRAINING_DATA_NAME = "GermanDPR-XQA-HP"
EPOCH = 1
INDEX_PATH = f"backend/data/colbert/indexes/{BASE_MODEL_NAME}/{TRAINING_DATA_NAME}/epoch{EPOCH}"

if __name__ == "__main__":

    RAG = RAGPretrainedModel.from_index(INDEX_PATH)

    with open("backend/data/colbert/checkpoints/bert-base-german-cased/GermanDPR-XQA-HP/epoch1/vocab.txt", "r", encoding="utf-8") as tokens:
        lines = tokens.readlines()
        lines = [line[:-1] for line in lines]
        embeddings = [(token, list(RAG.model.inference_ckpt.bert.parameters())[0][i].detach().numpy()) for i, token in enumerate(lines)]
        df = pd.DataFrame(embeddings, columns=["token", "embedding"])
        print(df.head(10))
        df.to_csv("embeddings.csv", index=False)
