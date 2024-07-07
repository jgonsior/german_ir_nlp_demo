import csv
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, SpectralClustering
from sklearn.metrics import silhouette_score

# Function to parse csv from given path;
# returns headers: first row of csv; position_data: dict[term,PCA components];
# ext_data: relict from test data, may require changes
def parse_csv(path):
    position_data = dict()
    ext_data = dict()

    with open(path, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        headers = next(reader)
        for row in reader:
            key = row[0]
            value = list(map(float, row[1:-1]))
            ext_value = value + [row[-1]]
            position_data[key] = value
            ext_data[key] = ext_value

    return headers, position_data, ext_data


# Function to write csv from clustered data to given path.
# The file's structure is identical to the file read in parse_csv(), the cluster labels are appended to every line.
def write_csv(path, headers, data, clustered_data, k_values):
    with open(path, mode='w', newline='') as clustered_file:
        writer = csv.writer(clustered_file, delimiter=',')
        writer.writerow(headers + [f'Cluster_k={k}' for k in k_values])
        for key, values in data.items():
            row = [key] + list(map(str, values)) + [str(clustered_data[k][key]) for k in k_values]
            writer.writerow(row)


# Function to find an estimation of the best number of clusters, based on k_means.
# The silhouette score is used for evaluation.
def find_best_k(raw_data, k_range):
    best_k = k_range[0]
    best_score = -1
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=0)
        kmeans.fit(raw_data)
        score = silhouette_score(raw_data, kmeans.labels_)
        if score > best_score:
            best_score = score
            best_k = k
    return best_k


# Function that applies k_means for a given k and returns a dictionary mapping labels to their respective terms.
def apply_kmeans(raw_data, k):
    data_values = np.array(list(raw_data.values()))
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(data_values)
    labels = kmeans.labels_
    return {key: labels[i] for i, key in enumerate(raw_data.keys())}


# Function that applies agglomerative_clustering for a given k, defaulting to ward linkage.
# It returns a dictionary mapping labels to their respective terms.
def apply_agglomerative_clustering(raw_data, k):
    data_values = np.array(list(raw_data.values()))
    agglomerative = AgglomerativeClustering(n_clusters=k, linkage='ward')
    labels = agglomerative.fit_predict(data_values)
    return {key: labels[i] for i, key in enumerate(raw_data.keys())}


# Function that applies spectral clustering for a given k, defaulting to nearest neighbors affinity.
# It returns a dictionary mapping labels to their respective terms.
def apply_spectral_clustering(raw_data, k):
    data_values = np.array(list(raw_data.values()))
    spectral = SpectralClustering(n_clusters=k, affinity='nearest_neighbors', random_state=0)
    labels = spectral.fit_predict(data_values)
    return {key: labels[i] for i, key in enumerate(raw_data.keys())}


if __name__ == '__main__':
    # User mini-guide:
    # The range specified in range_k_clusters as well as the list of values of interest in k_values can be edited
    # freely to change the number of clusters k that should be worked with.
    # Source and Target paths for CSV files can be changed in the function calls for parse_csv() and write_csv().

    # Specify the search space for the best fitting value for k
    range_k_clusters = range(2, 20)
    headers, data, extended_data = parse_csv('sample_data1.csv')

    optimal_k = find_best_k(np.array(list(data.values())), range_k_clusters)
    print(f'Optimal number of clusters: {optimal_k}')

    # List to store the all values for k to be used in clustering.
    k_values = [optimal_k, optimal_k - 2, optimal_k - 4, optimal_k + 2, optimal_k + 4, optimal_k + 6, optimal_k + 8]
    k_values = [k for k in k_values if k in range_k_clusters and k > 1]  # Ensure k > 1 and within range

    kmeans_clustered_data = {k: apply_kmeans(data, k) for k in k_values}
    agglomerative_clustered_data = {k: apply_agglomerative_clustering(data, k) for k in k_values}
    spectral_clustered_data = {k: apply_spectral_clustering(data, k) for k in k_values}

    # write the results of clustering into separate csv files
    write_csv('kmeans_clustered_data.csv', headers, extended_data, kmeans_clustered_data, k_values)
    write_csv('agglomerative_clustered_data.csv', headers, extended_data, agglomerative_clustered_data, k_values)
    write_csv('spectral_clustered_data.csv', headers, extended_data, spectral_clustered_data, k_values)
