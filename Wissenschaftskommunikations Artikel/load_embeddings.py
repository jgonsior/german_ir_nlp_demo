import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA

df = pd.read_csv("Wissenschaftskommunikations Artikel/colored_embeddings.csv.csv")

df["embedding"] = df["embedding"].apply(lambda x: np.fromstring(x.strip("[]"), sep=" "))

arr = np.vstack(df["embedding"])

decomp = PCA(
    n_components=100,
).fit_transform(arr)


plt.figure(figsize=(15, 4))
sns.heatmap(
    [decomp[0], decomp[1], decomp[2], decomp[3], decomp[4], decomp[5], decomp[6], decomp[7], decomp[8], decomp[9], decomp[10], decomp[11]],
    cmap=sns.color_palette("coolwarm", as_cmap=True),
    cbar=True,
    xticklabels=False,
    yticklabels=[
        "Harry",
        "Potter",
        "Hermine",
        "Hexe",
        "Hexen",
        "Zauberer",
        "Dumbledore",
        "Schulleiter",
        "Waschmaschine",
        "Fernseher",
        "Mikrowelle",
        "Wolfgang",
    ],
    linewidths=1,
)

plt.yticks(rotation=0)
# plt.savefig("Wissenschaftskommunikations Artikel/word2vec.pdf", dpi="figure", format="pdf")

plt.show()
