import numpy as np
import pandas as pd
import transformers as tf

tokenizer = tf.BertTokenizer.from_pretrained("backend/data/colbert/checkpoints/bert-base-german-cased/GermanDPR-XQA-HP/epoch1")
df_embeddings = pd.read_csv("embeddings.csv")

# Preprocess df_embeddings
df_embeddings["embedding"] = df_embeddings["embedding"].apply(lambda x: np.fromstring(x.strip("[]"), sep=" "))


def embed_word(tokenizer: tf.BertTokenizer, df: pd.DataFrame, word: str) -> np.ndarray:
    tokens = tokenizer(word)["input_ids"][1:-1]
    embedding = df["embedding"].iloc[tokens].mean()
    return embedding


with open("words_to_embed.txt", "r") as file:
    words = [line.strip() for line in file]

results = [(word, embed_word(tokenizer=tokenizer, df=df_embeddings, word=word)) for word in words]

results_df = pd.DataFrame(results, columns=["word", "embedding"])
results_df.to_csv("unity.csv", index=False)
