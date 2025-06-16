''' Question-2:- Eigenfaces-Face classification using PCA (40 classes)

a) Use the following “face.csv” file to classify the faces of 40 different people using PCA.

b) Do not use the in-built function for implementing PCA.

c) Use appropriate classifier taught in class (use any classification algorithm taught in class like Bayes classifier, minimum distance classifier, and so on)

d) Refer to the following link for a description of the dataset: https://towardsdatascience.com/eigenfaces-face-classification-in-python-7b8d2af3d3ea

'''
import numpy as np

# Step 1: Load and prepare the dataset
# Load the "face.csv" dataset
data = pd.read_csv("face.csv")
X = data.drop('target', axis=1).to_numpy()

# Step 2: Normalize the data
mean = np.mean(X, axis=0)
X_normalized = X - mean

# Step 3: Calculate the covariance matrix
covariance_matrix = np.cov(X_normalized, rowvar=False)

# Step 4: Calculate eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)

# Step 5: Sort eigenvalues and corresponding eigenvectors
sorted_indices = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[sorted_indices]
eigenvectors = eigenvectors[:, sorted_indices]

# Step 6: Choose the number of principal components (eigenfaces)
n_components = 100  # Adjust as needed
selected_eigenvectors = eigenvectors[:, :n_components]

# Step 7: Project the data onto the selected eigenvectors
X_pca = X_normalized.dot(selected_eigenvectors)

# Continue with classification using the projected data