import os
import torch
from flask import current_app
from transformers import AutoTokenizer, AutoModel
from ragatouille import RAGPretrainedModel
import numpy as np

class RagatouilleModelManager:
    def __init__(self):

        base_model_name = "bert-base-german-cased"

        self.tokenizer = AutoTokenizer.from_pretrained(base_model_name)
        self.model = AutoModel.from_pretrained(base_model_name)

        # TODO
        index_path = ''
        # self.model = RAGPretrainedModel.from_index(index_path)
        # self.model = AutoModel.from_pretrained(index_path)


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


if __name__ == '__main__':

    model_manager = RagatouilleModelManager()
    text = "Wer hat Snape umgebracht?"
    embeddings = model_manager.get_word_embeddings(text)

    for word, embedding in embeddings.items():
        print(f"Wort: {word}, Embedding: {embedding}")
