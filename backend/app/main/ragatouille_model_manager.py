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

        self.model = AutoModel.from_pretrained(checkpoint_path)
        self.rag_model = RAGPretrainedModel.from_index(index_path)

        # initial request to load the model
        self.rag_model.search('Initial Request', k=1)


    def search(self, query, k):
        results = self.rag_model.search(query=query, k=k)
        return results


    def get_word_embeddings(self, text):
        inputs = self.tokenizer(text, return_tensors='pt')
        with torch.no_grad():
            outputs = self.model(**inputs)


        token_embeddings = outputs.last_hidden_state[0]
        tokens = self.tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
        words = text.split()

        word_embeddings = {}
        word_tokens = []
        current_word = ""

        for token, embedding in zip(tokens, token_embeddings):
            if token.startswith("##"):
                current_word += token[2:]
            else:
                if current_word:
                    word_embeddings[current_word] = embedding.tolist()
                current_word = token
                word_tokens = [embedding]
                continue
            word_tokens.append(embedding)

        if current_word:
            word_embeddings[current_word] = embedding.tolist()

        return word_embeddings


def create_ragatouille_model_manager(index_path, model_path):
    return RagatouilleModelManager(index_path, model_path)
