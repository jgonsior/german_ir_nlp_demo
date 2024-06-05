import transformers as tf
import numpy as np
import pandas as pd

tokenizer = tf.BertTokenizer.from_pretrained("backend/data/colbert/checkpoints/bert-base-german-cased/GermanDPR-XQA-HP/epoch1")

df = pd.read_csv("embeddings.csv")


def embed_word(tokenizer: tf.BertTokenizer, df: pd.DataFrame, word: str) -> np.ndarray:

    tokens = tokenizer(word)["input_ids"][1:-1]
    df["embedding"] = df["embedding"].apply(lambda x: np.fromstring(x.strip("[]"), sep=" "))
    embedding = df.iloc[tokens]["embedding"].mean()

    return embedding


print(embed_word(tokenizer=tokenizer, df=df, word="Hufflepuff"))


# print(embeddings.shape)
# print(embeddings.mean().shape)#.mean(axis=0))


# with open("backend/data/colbert/checkpoints/bert-base-german-cased/GermanDPR-XQA-HP/epoch1/vocab.txt", "r", encoding="utf-8") as tokens:
#     lines = tokens.readlines()

# lines = [line[:-1] for line in lines]


# embeddings = [(token, list(RAG.model.inference_ckpt.bert.parameters())[0][i].detach().numpy()) for i, token in enumerate(lines)]
# df = pd.DataFrame(embeddings, columns=["token", "embedding"])
# print(df.head(10))

# df.to_csv("embeddings.csv", index=False)
