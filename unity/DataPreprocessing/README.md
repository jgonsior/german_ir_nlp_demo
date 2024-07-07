# german_ir_nlp_demo

## Data Preprocessing

The scripts `DataClustering.py` and  `EmbeddingPreprocessing` provide functionality for downsampling and clustering the word embedding data. The accordingly fitting script is to be applied to the data to then provide the resulting file(s) as input to the Unity application.

### DataClustering

`DataClustering.py` takes a specified CSV file of word embedding data and parses it. On the basis of K-Means, an optimal number of clusters is determined in a range of 2 to 20. The clustering algorithms **K-Means**, **Agglomerative Clustering** and **Spectral Clustering** are applied and the resulting cluster labels are appended to each data point. If multiple cluster sizes are specified, they are appended in the order they are specified in. The results are then saved into separate CSV files for each clustering method.  

The field `ext_data` was previously used but has become obsolte due to a change in input data structure. It was not been removed yet but holds no functional value.

This scipt does not include downsampling methods. 

### EmbeddingPreprocessing

`EmbeddingPreprocessing.py` combines downsampling with clustering fuctionality. A specified CIV file containing word embedding data is loaded into a DataFrame and the data's dimensionality is reduced to three by applying **Principal Component Analysis (PCA)**. 
The best-fitting K for K-Means is calculated and the the clustering results for **K-Means**, **AgglomerativeClustering** and **SpectralClustering** are written as new columns, together with the downsampled data to a CSV file.

A shortened version of `DataClustering.py` was introduced into this script for the final project as the availability of diverse clustering results was not needed. More specifically, the option to calculate multiple cluster sizes at once was removed. 

### Ìnput and Output Data
The correct formatting for input data files can be retrieved from the respective example files `example_data_clustering` for the `DataClustering.py` (please note the necessity of a header row) script and `example_data_embeddings` for `EmbeddingPreprocessing.py`.
The output file should be placed in the `\Assets\Scripts` folder and can then be applied to the respective script in the Inspector of the `scripts` object in Unity by drag and drop into the `Sample_data` field.