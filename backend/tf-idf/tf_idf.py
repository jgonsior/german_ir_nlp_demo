import json
import nltk
import math 
import numpy as np
import webbrowser

class tfIdf:
    all_tokens = set()

    def __init__(self):
        with open("harry_potter.json", "r") as read_file:
            self.data = json.load(read_file)
        self.all_tokens = self.find_all_tokens(self.data)

    def return_url(self, name):
        for document in self.data:
            if(name == document.get("title")):
                print(document.get("url"))
                webbrowser.open(document.get("url"))

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
                new_text = new_text + word.lower() + ""
        return new_text
    
    def find_all_tokens(self, data):
        all_tokens = set()
        for document in data:
            for sentence in document.get("text"):
                tokens = nltk.word_tokenize(self.remove_unimportant_symbols(sentence))
                for token in tokens:
                    all_tokens.add(token)
        return all_tokens
    
    def copy_dic(self, dic):
        copy_dic = {}
        for i in dic:
            copy_dic[i] = dic[i]

        return copy_dic
    
    def find_tf_idf_weight(self):

        all_tokens_dic = {}
        for token in self.all_tokens:
            all_tokens_dic[token] = 0

        #find tf value for the words in each file
        tf_dict = {}
        self.idf_dic = self.copy_dic(all_tokens_dic)
        df_dic = self.copy_dic(all_tokens_dic)

        count = 0

        for document in self.data:
            used_tokens = set()
            new_all_tokens_dic = self.copy_dic(all_tokens_dic)
            for sentence in document.get("text"):
                tokens = nltk.word_tokenize(self.remove_unimportant_symbols(sentence))
                for token in tokens:
                    new_all_tokens_dic[token] = new_all_tokens_dic[token] + 1
                    if token not in used_tokens:
                        df_dic[token] = df_dic[token] + 1
                        used_tokens.add(token)

            for token in new_all_tokens_dic:
                if(new_all_tokens_dic[token] > 0):
                    new_all_tokens_dic[token] = 1 + math.log10(new_all_tokens_dic[token])
            
            tf_dict[document.get("title")] = new_all_tokens_dic
            count = count + 1
            if count % 350  == 0:
                print("complete on " + str(count * 100/4478) +"%")

        for token in self.idf_dic:
            self.idf_dic[token] = math.log10(count / df_dic[token]) 

        print("complete + count: " + str(count))

        #find tf-idf vectors 
        tf_idf_dic = tf_dict
        for document in tf_idf_dic:
            current_docu = tf_idf_dic[document]
            current_vector = []
            for token in current_docu:
                current_vector.append(current_docu[token] * self.idf_dic[token])
            tf_idf_dic[document] = self.normalize_vector(np.array(current_vector))

        #with open("tf_idf_result.json", "w") as outfile: 
        #    json.dump(tf_idf_dic, outfile)

        print("Dolores Umbridges Zauberstab")
        for i in tf_idf_dic["Dolores Umbridges Zauberstab"]:
            if i > 0.004476071371261539:
                print(i, end = " ")
        print("Ronald Weasleys erster Zauberstab")
        for i in tf_idf_dic["Ronald Weasleys erster Zauberstab"]:
            if i > 0.004476071371261539:
                print(i, end = " ")
        return tf_idf_dic
    
    def find_query_tf_idf(self, data):

        all_tokens_dic = {}
        for token in self.all_tokens:
            all_tokens_dic[token] = 0

        tokens = nltk.word_tokenize(self.remove_unimportant_symbols(data))
        for token in tokens:
            all_tokens_dic[token] = all_tokens_dic[token] + 1

        for token in all_tokens_dic:
            if(all_tokens_dic[token] > 0):
                all_tokens_dic[token] = 1 + math.log10(all_tokens_dic[token])
            
        current_vector = []
        for token in all_tokens_dic:
            current_vector.append(all_tokens_dic[token] * self.idf_dic[token])
        norm_vector = self.normalize_vector(np.array(current_vector))

        return norm_vector