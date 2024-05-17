import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
import spacy
import json

def clean_tokens(tokenlist, normalize: bool = True):
    remove_chars = ['"', ',', '.', '[', ']', '{', '}', '(', ')', ':', '-', ';', "'", "!", '“', '„', '&', "''", "'s", '*', '...', '):', '/', '--', '---']
    tokens_filtered = [token.lower() for token in tokenlist if token not in remove_chars]        

    stemmer = SnowballStemmer("german")
    stop_words = set(stopwords.words("german"))
    if normalize: 
        tokens = [stemmer.stem(token) for token in tokens_filtered if token not in stop_words]
        tokens = [stemmer.stem(token) for token in tokens if token not in stop_words]
    else:
        tokens = [token for token in tokens_filtered]

    return tokens


def calculate_inverted_index(wiki_pages, output: str, normalize: bool = True):
        inverted_index = {}
        #lemmas = set()
        nlp = spacy.load("de_core_news_sm")

        with open('backend/inv_index/harry_potter.json', 'r') as file:
            data = json.load(file)

        for document in data:
            title = document['title']

            if title in wiki_pages:
                
                if normalize:
                    raw_tokens = set(str(token.lemma_.lower()) for token in nlp(document["text"]))
                    raw_tokens = set(str(token.lemma_.lower()) for token in nlp(" ".join(raw_tokens)))
                else:
                    raw_tokens = set(nltk.word_tokenize(document["text"]))

                tokens = clean_tokens(raw_tokens, normalize)

                #lemmas.update(set((token, token.lemma_) for token in nlp(" ".join(tokens))))

                if document['title'] not in inverted_index.keys():
                    inverted_index[title] = {}

                for token in tokens:
                    if token not in inverted_index[title]:
                        inverted_index[title][token] = []
                    if document['_id'] not in inverted_index[title][token]:
                        inverted_index[title][token].append(document['_id'])

        #sorted(lemmas)
        #lemmas = '{' + ', '.join(map(str, lemmas)) + '}'

        # with open('backend/inv_index/lemma.txt', 'w') as f:
        #     f.write(lemmas)

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
    calculate_inverted_index(wiki_pages, output, True)

    #tokens = get_all_tokens(output)
    # tokens_double = get_all_tokens("inv_index_double_Harry.json")
    #tokens.sort()
    # tokens_double.sort()
    #print(tokens)
    # print(tokens_double)
    #print(len(tokens))
    # print(len(tokens_double))
    # rem_token1 = [token for token in tokens if token not in tokens_double]
    # rem_token2 = [token for token in tokens_double if token not in tokens]
    # print(rem_token1)
    # print(rem_token2)
    # print(len(rem_token1))
    # print(len(rem_token2))