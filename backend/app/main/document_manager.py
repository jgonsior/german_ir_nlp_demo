from random import randint
import numpy as np
import json
import os
import re


FILENAME = "preprocessing/data/harry_potter_unicode_processed.json"


class DocumentManager:
    def __init__(self):
        with open(os.path.join(os.getcwd(), FILENAME), encoding="utf-8", mode="r") as f:
            self.documents = json.load(f)


    def get_document_by_id(self, doc_id):
        for d in self.documents:
            if int(doc_id) == int(d.get('id')):
                print(doc_id)
                return d


    def get_random_documents(self, amount):
        """
        return random pages
        """
        response = []
        indices_rand = np.random.randint(len(self.documents), size=amount)
        for index in indices_rand:
            page = self.documents[randint(0, len(self.documents)-1)]
            response.append(page)
        return self.to_json(response)


    def to_json(self, p):
        counter = 0
        resp = {
            "search_id" : randint(0, 100),
            "answers" : []
        }

        for page in p:
            page['rank'] = counter
            tmp = resp['answers']
            tmp.append(page)
            resp['answers'] = tmp
            counter += 1

        return  resp
