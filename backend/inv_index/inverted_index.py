import nltk
import json

def clean_tokens(tokenlist):
    remove_chars = ['"', ',', '.', '[', ']', '{', '}', '(', ')', ':']
    tokens = [token.lower() for token in tokenlist if token not in remove_chars]        

    return tokens

def calculate_inverted_index():
        inverted_index = {}

        with open('backend/inv_index/harry_potter.json', 'r') as file:
            data = json.load(file)

        for document in data:
            title = document['title']
            raw_tokens = set(nltk.word_tokenize(document["text"]))
            tokens = clean_tokens(raw_tokens)

            if document['title'] not in inverted_index.keys():
                 inverted_index[title] = {}

            for token in tokens:
                if token not in inverted_index[title]:
                    inverted_index[title][token] = []
                inverted_index[title][token].append(document['id'])

        with open('backend/inv_index/inverted_index.json', 'w', encoding="utf-8") as output:
                json.dump(inverted_index, output, indent=1, ensure_ascii=False)

def get_all_tokens():
    with open('backend/inv_index/inverted_index.json', 'r', encoding="utf-8") as file:
        data = json.load(file)
    
    return data.keys()


if __name__ == '__main__':
    #calculate_inverted_index()
    print(get_all_tokens())