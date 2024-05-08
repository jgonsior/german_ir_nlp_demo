import json
import nltk
import math 
import numpy as np

class tfIdf:

    def __init__(self):
        print("created")

    def normalize_vector(self, vector):
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm
    
    def remove_unimportant_symbols(self, text):
        unimportant_symbols = ['"', ',', '.', '[', ']', '{', '}', '(', ')', ':', ':']
        new_text = ""
        for word in text:
            if word not in unimportant_symbols:
                new_text = new_text + word + ""
        return new_text
    
    def find_all_tokens(self, data):
        all_tokens = set()
        for document in data:
            for sentence in document.get("text"):
                tokens = nltk.word_tokenize(self.remove_unimportant_symbols(sentence))
                for token in tokens:
                    all_tokens.add(token)
        return all_tokens
    
    def find_tf_idf_weight(self):

        with open("harry_potter.json", "r") as read_file:
            data = json.load(read_file)

        #find all tokens in data
        all_tokens = self.find_all_tokens(data)

        all_tokens_dic = {}
        for token in all_tokens:
            all_tokens_dic[token] = 0

        #find tf value for the words in each file
        tf_dict = {}
        idf_dic = all_tokens_dic
        df_dic = all_tokens_dic

        count = 0

        for document in data:
            used_tokens = set()
            new_all_tokens_dic = all_tokens_dic
            for sentence in document.get("text"):
                tokens = nltk.word_tokenize(self.remove_unimportant_symbols(sentence))
                for token in tokens:
                    new_all_tokens_dic[token] = new_all_tokens_dic[token] + 1
                    if token not in used_tokens:
                        df_dic[token] = df_dic[token] + 1
                        used_tokens.add(token)
            used_tokens = set()

            for token in new_all_tokens_dic:
                if(new_all_tokens_dic[token] > 0):
                    new_all_tokens_dic[token] = 1 + math.log10(new_all_tokens_dic[token])
            
            tf_dict[document.get("title")] = new_all_tokens_dic
            count = count + 1
            if count % 350  == 0:
                print("complete on " + str(count * 100/4478) +"%")

        for token in idf_dic:
            idf_dic[token] = math.log10(count / df_dic[token]) 

        print("complete + count: " + str(count))

        #find tf-idf vectors 
        tf_idf_dic = tf_dict
        for document in tf_idf_dic:
            current_docu = tf_idf_dic[document]
            current_vector = []
            for token in current_docu:
                current_vector.append(current_docu[token] * idf_dic[token])
            tf_idf_dic[document] = self.normalize_vector(np.array(current_vector))

        #with open("tf_idf_result.json", "w") as outfile: 
        #    json.dump(tf_idf_dic, outfile)
        return tf_idf_dic