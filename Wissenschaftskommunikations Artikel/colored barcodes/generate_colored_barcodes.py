import os

import matplotlib.pyplot as plt
import seaborn as sns
from gensim.models import Word2Vec

# Has the structure ("question", "answer", "answer-passage-ID")

terms_to_display = [
    ("harry", "potter", "1-221"),
    ("zauberer", "hexen", "1-1"),
    ("dumbledore", "schulleiter", "1-46"),
    ("hufflepuff", "branstone", "1-144"),
    ("tom", "riddle", "2-1"),
    ("malfoy", "draco", "2-68"),
    ("bellatrix", "lestrange", "2-55"),
    ("ariana", "aberforth", "2-59"),
    ("dolores", "umbridge", "2-73"),
    ("flitwick", "filius", "6-1"),
    ("sirius", "severus", "6-2"),
    ("alexia", "walkin", "6-77"),
    ("peter", "pettigrew", "6-78"),
    ("phönixfeder", "kern", "4-2"),
    ("dobby", "hauself", "4-69"),
    ("schneeeule", "hedwig", "4-8"),
    ("lilly", "beschuldigung", "4-60"),
    ("orden", "phönix", "4-78"),
    ("adalbert", "schwahfel", "4-13"),
    ("george", "fred", "5-1"),
    ("slughorn", "horace", "5-20"),
    ("heiligtümer", "todes", "3-1"),
    ("daniel", "radcliffe", "3-117"),
    ("emma", "watson", "3-12"),
    ("kammer", "schreckens", "3-24"),
    ("drachenherzfaser", "weißbuche", "3-2"),
    ("viktor", "krum", "3-200"),
]

def _ensure_directiory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def save_plot(path_to_save: str, idx: str | int):
    plt.savefig(
        f"{path_to_save}_{idx}.svg",
        dpi="figure",
        format="svg",
        bbox_inches="tight",
        pad_inches=0,
    )
    plt.close()


def generate_embedding_for_term(model: Word2Vec, term: str, idx: int | str, questions_set: bool = False, answers_set: bool = False):
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
            generate_embedding_for_term(model=model, term=term_pair[1], idx=term_pair[2], answers_set=generate_answers)


if __name__ == "__main__":
    # Load the model
    model = Word2Vec.load("Wissenschaftskommunikations Artikel/colored barcodes/harry_potter_german_word2vec.model")

    plot_embeddings(model=model,generate_questions=True, generate_answers=True)
