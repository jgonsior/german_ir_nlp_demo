import numpy as np
import json
from . import tf_idf


class queryFinder:
    def __init__(self):
        self.tf_idf_class = tf_idf.TfIdf()
        self.tf_idf_docu_dic = self.tf_idf_class.find_tf_idf_weight()
        print("tf-idf vectors found")

        # inverted index will be stored as inverted_index.json
        self.tf_idf_class.calculate_inverted_index()


    def query_vector_finder(self, query, num):
        query_vector = self.tf_idf_class.find_query_tf_idf(query)

        dict_ind = {}

        for name_docu in self.tf_idf_docu_dic:
            current_value = self.tf_idf_docu_dic[name_docu] * query_vector
            count = 0
            for value in current_value:
                count = count + value
            dict_ind[name_docu] = count

        list_key = list(dict_ind.keys())
        list_ind = list(dict_ind.values())
        
        for i in range(len(list_ind)):
            for j in range(i, len(list_ind)):
                if(list_ind[i] < list_ind[j]):
                    temp = list_ind[i]
                    list_ind[i] = list_ind[j]
                    list_ind[j] = temp
                    temp_str = list_key[i]
                    list_key[i] = list_key[j]
                    list_key[j] = temp_str

        list_answer = []
        for i in range(num):
            print(list_ind[i])
            print(list_key[i])
            list_answer.append(self.tf_idf_class.return_url(list_key[i], i))

        dict_answ = {} #answer
        dict_answ["answer"] = list_answer

        # self.generate_answer(dict_answ)
        return dict_answ

    """
    # answer can be saved as json
    def generate_answer(self, dict):
        with open("answer.json", "w", encoding="utf-8") as outfile:
            json.dump(dict, outfile, ensure_ascii=False, indent=4)
    """
