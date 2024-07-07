import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, SpectralClustering
from sklearn.metrics import silhouette_score
import ast

# Load the dataframe
df = pd.read_csv("")  # Todo: Specify your filepath here

n_components = 3

# Convert embedding strings to list
df['embedding'] = df['embedding'].apply(ast.literal_eval)

# Convert embeddings column to numpy array
embeddings = np.array(df['embedding'].tolist())

# Apply PCA to downsample the embeddings
pca = PCA(n_components=n_components)
reduced_embeddings = pca.fit_transform(embeddings)

# Update dataframe with reduced embeddings
df['embedding'] = reduced_embeddings.tolist()
df[['x', 'y', 'z']] = pd.DataFrame(df['embedding'].tolist(), index=df.index)
df = df.drop('embedding', axis=1)

# Function to find an estimation of the best number of clusters, based on k_means.
# The silhouette score is used for evaluation.
def find_best_k(data, k_range):
    best_k = k_range[0]
    best_score = -1
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=0)
        kmeans.fit(data)
        score = silhouette_score(data, kmeans.labels_)
        if score > best_score:
            best_score = score
            best_k = k
    return best_k

# Function to apply KMeans clustering
def kmeans_cluster(n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    return kmeans.fit_predict(reduced_embeddings)

# Function to apply Agglomerative clustering
def agglomerative_cluster(n_clusters):
    agglomerative = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward')
    return agglomerative.fit_predict(reduced_embeddings)

# Function to apply Spectral clustering
def spectral_cluster(n_clusters):
    spectral = SpectralClustering(n_clusters=n_clusters, affinity='nearest_neighbors', random_state=0)
    return spectral.fit_predict(reduced_embeddings)


# Define range of k for finding the optimal number of clusters
range_k_clusters = range(2, 20)
optimal_k = find_best_k(reduced_embeddings, range_k_clusters)
print(f'Optimal number of clusters for KMeans: {optimal_k}')

# List to store the all values for k to be used in clustering.
# append additional values for k if needed.
k_values = [optimal_k]

# Apply KMeans clustering with the optimal number of clusters
for k in k_values:
    df[f'kmeans_{k}'] = kmeans_cluster(k)

# Apply Agglomerative clustering with the optimal number of clusters
for k in k_values:
    df[f'agglomerative_{k}'] = agglomerative_cluster(k)

# Apply Spectral clustering with the optimal number of clusters
for k in k_values:
    df[f'spectral_{k}'] = spectral_cluster(k)

# Save the results to a new CSV file
df.to_csv("", index=False)  # Todo: Specify your filepath here


