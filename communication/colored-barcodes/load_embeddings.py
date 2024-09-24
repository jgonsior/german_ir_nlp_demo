import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.decomposition import PCA

df = pd.read_csv("embeddings.csv")

df["embedding"] = df["embedding"].apply(lambda x: np.fromstring(x.strip("[]"), sep=" "))

arr = np.vstack(df["embedding"])

decomp = PCA(n_components=100).fit_transform(arr)


plt.figure(figsize=(15, 4))
sns.heatmap(
    [decomp[0], decomp[1]],
    cmap=sns.color_palette("coolwarm", as_cmap=True),
    cbar=True,
    xticklabels=False,
    yticklabels=["harry", "potter", ""],
    linewidths=1,
)

plt.yticks(rotation=0)
# plt.savefig("communication/word2vec.pdf", dpi="figure", format="pdf")

plt.show()
