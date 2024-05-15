import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
import spacy
import json

def clean_tokens(tokenlist):

    remove_chars = ['"', ',', '.', '[', ']', '{', '}', '(', ')', ':', '-', ';', "'", "!", '“', '„', '&', "''", "'s", '*', '...', '):', '/', '--']
    tokens_filtered = [token.lower() for token in tokenlist if token not in remove_chars]        

    stemmer = SnowballStemmer("german")
    stop_words = set(stopwords.words("german"))
    tokens_stemmed = [stemmer.stem(token) for token in tokens_filtered if token not in stop_words]

    return tokens_stemmed

def calculate_inverted_index(wiki_pages, output: str):
        inverted_index = {}
        #lemmas = set()
        nlp = spacy.load("de_core_news_sm")

        with open('backend/inv_index/harry_potter.json', 'r') as file:
            data = json.load(file)

        for document in data:
            title = document['title']

            if title in wiki_pages:
                #raw_tokens = set(nltk.word_tokenize(document["text"]))

                raw_tokens = [str(token.lemma_) for token in nlp(document["text"])]

                #lemmas.update([(token, token.lemma_) for token in nlp(document["text"])])

                tokens = clean_tokens(raw_tokens)

                if document['title'] not in inverted_index.keys():
                    inverted_index[title] = {}

                for token in tokens:
                    if token not in inverted_index[title]:
                        inverted_index[title][token] = []
                    inverted_index[title][token].append(document['_id'])

        # sorted(lemmas)
        # print(lemmas)

        with open(f'backend/inv_index/{output}', 'w', encoding="utf-8") as output:
                json.dump(inverted_index, output, indent=1, ensure_ascii=False)

def get_all_tokens(file):
    tokens = []
    with open(f'backend/inv_index/{file}', 'r', encoding="utf-8") as file:
        data = json.load(file)
 
    for obj in data.values():
        tokens.extend(obj.keys())
    
    return tokens


if __name__ == '__main__':
    wiki_pages=["Harry Potter"]
    output = "inv_index_Harry.json"
    calculate_inverted_index(wiki_pages, output)
    tokens = get_all_tokens("inv_index_Harry.json")

    tokens.sort()
    print(tokens)
    print(len(tokens))