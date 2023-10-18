import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from scipy.spatial.distance import pdist, squareform
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.sparse import find
from sklearn.cluster import AgglomerativeClustering

iris = load_iris()                                   
data = iris.data[:, :2]                              

dist_matrix = squareform(pdist(data, metric='euclidean'))       

mst = minimum_spanning_tree(dist_matrix)                       

sorted_edges = sorted(zip(edges[0], edges[1], dist_matrix[edges[0], edges[1]]), key=lambda x: -x[2])
longest_edges = sorted_edges[:2]

clustered_edges = sorted_edges[2:]

agg_clustering = AgglomerativeClustering(n_clusters=3, linkage='ward')
agg_clustering.fit(data)

plt.figure(figsize=(10, 6))
for i, j, _ in clustered_edges:
    plt.plot([data[i, 0], data[j, 0]], [data[i, 1], data[j, 1]], 'k-', lw=0.5)
for i in range(data.shape[0]):
    plt.text(data[i, 0], data[i, 1], str(agg_clustering.labels_[i]),
             color=plt.cm.nipy_spectral(agg_clustering.labels_[i] / 3.),
             fontdict={'weight': 'bold', 'size': 9})

plt.title("Minimum Spanning Tree with Clusters")
plt.scatter(data[:, 0], data[:, 1], c=agg_clustering.labels_, cmap='viridis')
plt.show()
