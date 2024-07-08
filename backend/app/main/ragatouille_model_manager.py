import os
import torch
from flask import current_app
from transformers import AutoTokenizer, AutoModel
from ragatouille import RAGPretrainedModel

import numpy as np

from . import utils

print('------------------------------')
print('Is Cua available?')
print(torch.cuda.is_available())
print('------------------------------')

class RagatouilleModelManager:
    def __init__(self, index_path, checkpoint_path):

        # base_model_name = "bert-base-german-cased"

        # Update metadata.json (checkpoint path)
        # check config.ini for defined paths
        utils.update_model_metadata(index_path, checkpoint_path)

        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)

        self.model = AutoModel.from_pretrained(checkpoint_path)
        self.rag_model = RAGPretrainedModel.from_index(index_path)

        print('Initial Request to preload some data')
        # initial request to load the model
        self.rag_model.search('Initial Request', k=1)


    def search(self, query, k):
        results = self.rag_model.search(query=query, k=k)
        return results


    def get_embeddings(self,text):
        inputs = self.tokenizer(text, return_tensors='pt')
        with torch.no_grad():
            outputs = self.model(**inputs)


        token_embeddings = outputs.last_hidden_state[0]
        tokens = self.tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
        return token_embeddings, tokens


    def merge_tokens(self, tokens, token_scores):
        words = []
        scores = []
        current_word = ""
        acc_score = 0
        for token, token_score in zip(tokens, token_scores):
            if token.startswith("##"):
                current_word += token[2:]
                acc_score += token_score
            else:
                if current_word:
                    words.append(current_word)
                    scores.append(acc_score)

                current_word = token
                acc_score = token_score
        if current_word:
            words.append(current_word)
            scores.append(acc_score)

        return words, scores


    def compute_similarity(self, query_embeddings, passage_embeddings):
        # Compute the similarity matrix using dot product
        sim_matrix = np.dot(query_embeddings, passage_embeddings.T)
        return sim_matrix


    def colbert_scoring(self, query_embeddings, passage_embeddings, k=1):
        # Step 1: Compute the similarity matrix
        sim_matrix = self.compute_similarity(query_embeddings, passage_embeddings)

        # Step 2: Initialize a passage scores array to accumulate scores
        passage_scores = np.zeros(passage_embeddings.shape[0])

        # Step 3: For each query token, find the passage token with the highest similarity
        for i in range(sim_matrix.shape[0]):
            # Find the top k passage tokens with the highest similarity to the current query token
            top_k_indices = np.argsort(sim_matrix[i])[::-1][:k]

            # Add the similarity values to the corresponding passage token scores
            for pos, index in enumerate(top_k_indices):
                passage_scores[index] += sim_matrix[i, index] * (0.5**pos)

        return passage_scores


    def get_word_scores(self, query, passage, k=1):
        q_embeddings, q_tokens = self.get_embeddings(query)
        p_embeddings, p_tokens = self.get_embeddings(passage)
        p_scores = self.colbert_scoring(q_embeddings, p_embeddings, k=k)
        words, scores = self.merge_tokens(p_tokens[1:][:-1], p_scores[1:][:-1])
        # normalize word_scores
        scores = scores / max(scores)

        return words, scores


def create_ragatouille_model_manager(index_path, model_path):
    return RagatouilleModelManager(index_path, model_path)
