import json
import re
import string

import nltk
from gensim.models import Word2Vec
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download("stopwords")


def load_training_data(path_to_training_data: str) -> list[str]:
    # Load the JSON file
    with open(path_to_training_data, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Extract text data from JSON
    text_data = []
    for entry in data:
        text_data.extend(entry["text"])

    return text_data


# Preprocess the text
def preprocess_text(text_list) -> list[str]:
    stop_words = set(stopwords.words("german"))
    stemmer = WordNetLemmatizer()
    processed_text = []
    for text in text_list:
        # Remove text within brackets and punctuation, convert to lowercase
        text = re.sub(r"\[.*?\]", "", text)
        text = text.translate(str.maketrans("", "", string.punctuation))
        text = text.lower()
        # Tokenize, remove stop words, and stem
        tokens = word_tokenize(text)
        tokens = [stemmer.lemmatize(word) for word in tokens if word not in stop_words and word.isalpha()]
        processed_text.append(tokens)
    return processed_text


def train_word2vec(training_data: list[str], save: bool = False, path_to_save: str = "") -> Word2Vec:
    # Train Word2Vec model
    model = Word2Vec(
        sentences=training_data,
        vector_size=70,
        window=10,  # Context window size
        min_count=2,  # Minimum frequency for a word to be considered
        workers=8,  # Number of worker threads to train the model
        sg=1,  # Use skip-gram model
        hs=0,  # Use negative sampling
        negative=10,  # Number of negative samples
        epochs=10,  # Number of epochs
    )

    if save:
        model.save(f"{path_to_save}/harry_potter_german_word2vec.model")

    return model


def find_most_similar(model: Word2Vec, tokens: list[str]):
    for token in tokens:
        print(f"Most similar terms for the token {token}: \n {model.wv.most_similar(token.lower())}")


if __name__ == "__main__":
    training_data = load_training_data(path_to_training_data="backend/preprocessing/data/harry_potter_unicode_processed.json")
    preprocessed_training_data = preprocess_text(training_data)
    model = train_word2vec(training_data=preprocessed_training_data, save=True, path_to_save="Wissenschaftskommunikations Artikel/")
    find_most_similar(model, ["Harry", "Dumbledore", "Hermine"])
