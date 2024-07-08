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
    """
    Load training data from a JSON file.

    Args:
        path_to_training_data (str): The path to the JSON file containing the training data.

    Returns:
        list[str]: A list of text data extracted from the JSON file.
    """
    with open(path_to_training_data, "r", encoding="utf-8") as file:
        data = json.load(file)

    text_data = []
    for entry in data:
        text_data.extend(entry["text"])

    return text_data


def preprocess_text(text_list: list[str]) -> list[str]:
    """
    Preprocess a list of texts by removing punctuation, converting to lowercase, removing stop words,
    and lemmatizing.

    Args:
        text_list (list[str]): A list of text strings to preprocess.

    Returns:
        list[str]: A list of preprocessed text strings.
    """
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
    """
    Train a Word2Vec model on the given training data.

    Args:
        training_data (list[str]): A list of preprocessed text strings to use as training data.
        save (bool, optional): Whether to save the trained model to a file. Defaults to False.
        path_to_save (str, optional): The path to save the trained model if `save` is True. Defaults to "".

    Returns:
        Word2Vec: The trained Word2Vec model.
    """
    model = Word2Vec(
        sentences=training_data,
        vector_size=70, # Number of dimensions / barcodes stripes to be displayed
        window=10,      # Context window size
        min_count=2,    # Minimum frequency for a word to be considered
        workers=8,      # Number of worker threads to train the model
        sg=1,           # Use skip-gram model
        hs=0,           # Use negative sampling
        negative=10,    # Number of negative samples
        epochs=10,      # Number of epochs
    )


    if save:
        model.save(f"{path_to_save}/harry_potter_german_word2vec.model")

    return model


def find_most_similar(model: Word2Vec, tokens: list[str]) -> None:
    """
    Find and print the most similar terms for each token in the given list.

    Args:
        model (Word2Vec): The trained Word2Vec model.
        tokens (list[str]): A list of tokens for which to find similar terms.
    """
    for token in tokens:
        print(f"Most similar terms for the token {token}: \n {model.wv.most_similar(token.lower())}")


if __name__ == "__main__":
    training_data = load_training_data(path_to_training_data="backend/preprocessing/data/harry_potter_unicode_processed.json")
    preprocessed_training_data = preprocess_text(training_data)
    model = train_word2vec(training_data=preprocessed_training_data, save=True, path_to_save="Wissenschaftskommunikations Artikel/colored barcodes")
    find_most_similar(model, ["Harry", "Dumbledore", "Hermine"])
