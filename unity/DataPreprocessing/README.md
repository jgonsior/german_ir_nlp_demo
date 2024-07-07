# german_ir_nlp_demo

## Data Preprocessing

The scripts `DataClustering.py` and  `EmbeddingPreprocessing` provide functionality for downsampling and clustering the word embedding data. The accordingly fitting script is to be applied to the data to then provide the resulting file(s) as input to the Unity application.

### DataClustering

`DataClustering.py` takes a specified CSV file of word embedding data and parses it. On the basis of K-Means, an optimal number of clusters is determined in a range of 2 to 20. The clustering algorithms **K-Means**, **Agglomerative Clustering** and **Spectral Clustering** are applied and the resulting cluster labels are appended to each data point. If multiple cluster sizes are specified, they are appended in the order they are specified in. The results are then saved into separate CSV files for each clustering method.  

This scipt does not include downsampling methods. 

### EmbeddingPreprocessing

`EmbeddingPreprocessing.py` combines downsampling with clustering fuctionality. A specified CIV file containing word embedding data is loaded into a DataFrame and the data's dimensionality is reduced to three by applying **Principal Component Analysis (PCA)**. 
The best-fitting K for K-Means is calculated and the the clustering results for **K-Means**, **AgglomerativeClustering** and **SpectralClustering** are written as new columns, together with the downsampled data to a CSV file.

A shortened version of `DataClustering.py` was introduced into this script for the final project as the availability of diverse clustering results was not needed. More specifically, the option to calculate multiple cluster sizes at once was removed. 
