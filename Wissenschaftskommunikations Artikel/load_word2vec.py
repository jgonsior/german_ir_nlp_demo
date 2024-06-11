import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from gensim.models import Word2Vec

# Load the model
model = Word2Vec.load("Wissenschaftskommunikations Artikel/harry_potter_german_word2vec.model")

# Method of finding the most similar vector for a given term
# print(model.wv.most_similar("schwahfel"))

# Has the structure ("question", "answer")
terms_to_display = [
    ("harry", "potter"),
    ("zauberer", "hexen"),
    ("dumbledore", "schulleiter"),
    ("hufflepuff", "branstone"),
    ("tom", "riddle"),
    ("malfoy", "draco"),
    ("bellatrix", "lestrange"),
    ("ariana", "aberforth"),
    ("dolores", "umbridge"),
    ("flitwick", "filius"),
    ("sirius", "severus"),
    ("alexia", "walkin"),
    ("peter", "pettigrew"),
    ("phönixfeder", "kern"),
    ("dobby", "hauself"),
    ("schneeeule", "hedwig"),
    ("lilly", "beschuldigung"),
    ("orden", "phönix"),
    ("adalbert", "schwahfel"),
    ("george", "fred"),
    ("slughorn", "horace"),
    ("heiligtümer", "todes"),
    ("daniel", "radcliffe"),
    ("emma", "watson"),
    ("kammer", "schreckens"),
    ("drachenherzfaser", "weißbuche"),
    ("viktor", "krum"),
]


def plot_embeddings():

    for question_id, term_pair in enumerate(terms_to_display):
        question = term_pair[1]

        plt.figure(figsize=(15, 4))
        sns.heatmap(
            [model.wv[question]],
            cmap=sns.color_palette("coolwarm", as_cmap=True),
            cbar=False,
            xticklabels=False,
            yticklabels=False,
            linewidths=1,
        )
        # plt.show()
        plt.savefig(f"Wissenschaftskommunikations Artikel/answers/answer_{question_id}.svg", dpi="figure", format="svg")


plot_embeddings()
