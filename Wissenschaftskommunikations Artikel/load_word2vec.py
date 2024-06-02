import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from gensim.models import Word2Vec

# Load the model
model = Word2Vec.load("Wissenschaftskommunikations Artikel/harry_potter_german_word2vec.model")

print(model.wv.most_similar("dumbledore"))

plt.figure(figsize=(15, 4))
sns.heatmap(
    [
        model.wv["harry"],
        model.wv["potter"],
        model.wv["zauberer"],
        model.wv["hexen"],
        model.wv["hexe"],
    ],
    cmap=sns.color_palette("coolwarm", as_cmap=True),
    cbar=True,
    xticklabels=False,
    yticklabels=[
        "harry",
        "potter",
        "zauberer",
        "hexen",
        "hexe",
    ],
    linewidths=1,
)

# Rotate y-tick labels to 90 degrees
plt.yticks(rotation=0)

plt.show()
