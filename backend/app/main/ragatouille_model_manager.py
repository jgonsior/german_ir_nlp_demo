import os
import torch
from flask import current_app
from transformers import AutoTokenizer, AutoModel
from ragatouille import RAGPretrainedModel

from . import utils

class RagatouilleModelManager:
    def __init__(self, index_path, checkpoint_path):

        base_model_name = "bert-base-german-cased"
        self.index_path = index_path

        # Update metadata.json (checkpoint path)
        # check config.ini for defined paths
        utils.update_model_metadata(index_path, checkpoint_path)

        self.tokenizer = AutoTokenizer.from_pretrained(base_model_name)
        self.model = AutoModel.from_pretrained(base_model_name)

        self.rag_model = RAGPretrainedModel.from_index(index_path)


    def get_model_embeddings(self, text):
        inputs = self.tokenizer(text, return_tensors='pt')
        print('tokens:', inputs)
        print(self.tokenizer.convert_ids_to_tokens(inputs['input_ids'][0]))
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state


    def search(self, query, k):
        results = self.rag_model.search(query=query, k=k)
        return results


    def get_query_embeddings(self, query):
        return self.get_model_embeddings(query)


    def get_document_embeddings(self, documents):
        document_embeddings = []
        for doc in documents:
            doc_text = doc['passage']
            doc_embeddings = self.get_model_embeddings(doc_text)
            document_embeddings.append(doc_embeddings)
        return document_embeddings


def create_ragatouille_model_manager(index_path, model_path):
    return RagatouilleModelManager(index_path, model_path)
