import numpy as np
import tf_idf

str = "Arten von Holz, die für Herstellung von Zauberstäben benutzen sind"

class queryFinder:

    def __init__(self):
        self.tf_idf_class = tf_idf.tfIdf() 
        print("created")
        self.tf_idf_docu_dic = self.tf_idf_class.find_tf_idf_weight()
        print("tf-idf vectors found")

    def query_vector_finder(self):
        query_vector = self.tf_idf_class.find_query_tf_idf(str)

        maximum = 0
        docu_name = ""

        for name_docu in self.tf_idf_docu_dic:
            current_value = self.tf_idf_docu_dic[name_docu] * query_vector
            count = 0
            for value in current_value:
                count = count + value
            if(count > maximum):
                maximum = count
                docu_name = name_docu

        print(maximum)
        print(docu_name)
        self.tf_idf_class.return_url(docu_name)

queryFind = queryFinder()
queryFind.query_vector_finder()