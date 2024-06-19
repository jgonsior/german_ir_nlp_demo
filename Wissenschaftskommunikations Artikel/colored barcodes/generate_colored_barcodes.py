import os

import matplotlib.pyplot as plt
import seaborn as sns
from gensim.models import Word2Vec

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

def _ensure_directiory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def save_plot(path_to_save: str, idx: int):
    plt.savefig(
        f"{path_to_save}_{idx}.svg",
        dpi="figure",
        format="svg",
        bbox_inches="tight",
        pad_inches=0,
    )
    plt.close()


def generate_embedding_for_term(model: Word2Vec, term: str, idx: int, questions_set: bool = False, answers_set: bool = False):
    plt.figure(figsize=(15, 4))
    sns.heatmap(
        [model.wv[term]],
        cmap=sns.color_palette("coolwarm", as_cmap=True),
        cbar=False,
        xticklabels=False,
        yticklabels=False,
        linewidths=1,
    )
    plt.axis("off")

    if questions_set:
        _ensure_directiory_exists("Wissenschaftskommunikations Artikel/colored barcodes/questions")
        save_plot(path_to_save="Wissenschaftskommunikations Artikel/colored barcodes/questions/question", idx=idx)

    if answers_set:
        _ensure_directiory_exists("Wissenschaftskommunikations Artikel/colored barcodes/answers")
        save_plot(path_to_save="Wissenschaftskommunikations Artikel/colored barcodes/answers/answer", idx=idx)


def plot_embeddings(model: Word2Vec, generate_questions: bool, generate_answers: bool):
    for idx, term_pair in enumerate(terms_to_display):
        if generate_questions:
            generate_embedding_for_term(model=model, term=term_pair[0], idx=idx, questions_set=generate_questions)
        if generate_answers:
            generate_embedding_for_term(model=model, term=term_pair[1], idx=idx, answers_set=generate_answers)


if __name__ == "__main__":
    # Load the model
    model = Word2Vec.load("Wissenschaftskommunikations Artikel/colored barcodes/harry_potter_german_word2vec.model")

    plot_embeddings(model=model,generate_questions=True, generate_answers=True)
