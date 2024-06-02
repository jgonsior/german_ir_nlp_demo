import json
import re
import string

import nltk
from gensim.models import Word2Vec
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download("stopwords")

# Load the JSON file
with open("backend/preprocessing/data/harry_potter_unicode_processed.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract text data from JSON
text_data = []
for entry in data:
    text_data.extend(entry["text"])


# Preprocess the text
def preprocess_text(text_list):
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


processed_text = preprocess_text(text_data)

# Train Word2Vec model
model = Word2Vec(
    sentences=processed_text,
    vector_size=70,  # Increased vector size
    window=10,  # Context window size
    min_count=2,  # Minimum frequency for a word to be considered
    workers=8,  # Number of worker threads to train the model
    sg=1,  # Use skip-gram model
    hs=0,  # Use negative sampling
    negative=10,  # Number of negative samples
    epochs=10,  # Number of epochs
)

print(model.wv.most_similar("harry"))
print(model.wv.most_similar("dumbledore"))
print(model.wv.most_similar("hermine"))

# Save the model
model.save("Wissenschaftskommunikations Artikel/harry_potter_german_word2vec.model")
