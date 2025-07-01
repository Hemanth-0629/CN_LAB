''' QUESTION:- Consider the 128- dimensional feature vectors (d=128) given in the “gender.csv” file. (2 classes, male and female)

a) Use PCA to reduce the dimension from d to d‟. (Here d=128).

b) Display the eigenvalue based on increasing order, select the d‟ of the corresponding eigenvector which is the appropriate dimension d‟ ( select d‟ S.T first 95% of λ values of the covariance matrix are considered).

c) Use d‟ features to classify the test cases (use any classification algorithm taught in class like Bayes classifier, minimum distance classifier, and so on).


Dataset Specifications:

Total number of samples = 800

Number of classes = 2 (labeled as “male” and “female”)

Samples from “1 to 400” belongs to class “male”

Samples from “401 to 800” belongs to class “female”

Number of samples per class = 400

Number of dimensions = 128

Use the following information to design classifier:

Number of test cases (first 10 in each class) = 20

Number of training feature vectors ( remaining 390 in each class) = 390

Number of reduced dimensions = d‟ (map 128 to d‟ features vector) '''

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

# Load and prepare the dataset
data = pd.read_csv("gender.csv")
X = data.drop('class', axis=1).to_numpy()
y = data['class'].to_numpy()

# Separate data into male and female classes
X_male = X[:400]
X_female = X[400:]
y_male = y[:400]
y_female = y[400:]

# Split data into training and testing sets
X_train_male, X_test_male, y_train_male, y_test_male = train_test_split(X_male, y_male, test_size=10, random_state=42)
X_train_female, X_test_female, y_train_female, y_test_female = train_test_split(X_female, y_female, test_size=10, random_state=42)

# Calculate the mean of the training data
mean_male = np.mean(X_train_male, axis=0)
mean_female = np.mean(X_train_female, axis=0)

# Compute the covariance matrix of the centered training data
cov_male = np.cov(X_train_male - mean_male, rowvar=False)
cov_female = np.cov(X_train_female - mean_female, rowvar=False)

# Combine covariance matrices and calculate the mean covariance
total_cov = (cov_male + cov_female) / 2

# Calculate the eigenvalues and eigenvectors of the mean covariance matrix
eigenvalues, eigenvectors = np.linalg.eig(total_cov)

# Sort eigenvalues and corresponding eigenvectors in descending order
sorted_indices = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[sorted_indices]
eigenvectors = eigenvectors[:, sorted_indices]

# Determine d' for 95% explained variance
total_variance = np.sum(eigenvalues)
explained_variance_ratio = eigenvalues / total_variance
cumulative_variance_ratio = np.cumsum(explained_variance_ratio)
d_prime = np.argmax(cumulative_variance_ratio >= 0.95) + 1

# Reduce data dimension for both male and female classes
X_train_male_pca = (X_train_male - mean_male).dot(eigenvectors[:, :d_prime])
X_test_male_pca = (X_test_male - mean_male).dot(eigenvectors[:, :d_prime])
X_train_female_pca = (X_train_female - mean_female).dot(eigenvectors[:, :d_prime])
X_test_female_pca = (X_test_female - mean_female).dot(eigenvectors[:, :d_prime])

# Combine the reduced-dimension training data and labels
X_train_pca = np.vstack((X_train_male_pca, X_train_female_pca))
y_train_pca = np.concatenate((y_train_male, y_train_female))

# Classification (Naive Bayes classifier)
classifier = GaussianNB()


# Train the classifier on the reduced-dimensional training data
classifier.fit(X_train_pca, y_train_pca)


# Test the classifier on the reduced-dimensional test data
X_test_pca = np.vstack((X_test_male_pca, X_test_female_pca))
y_test_pca = np.concatenate((y_test_male, y_test_female))
y_pred = classifier.predict(X_test_pca)

# Calculate the accuracy of the classifier
accuracy = accuracy_score(y_test_pca, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")

