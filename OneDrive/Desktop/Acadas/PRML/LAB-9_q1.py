import numpy as np
import pandas as pd

# Load the dataset
data = pd.read_csv("gender.csv")
labels = data["label"]  # Assuming the labels are in a column named "label"
data = data.drop(columns=["label"])  # Remove the label column from the data

# Constants
d = 128  # Original dimensionality
d_prime = 2  # Desired reduced dimensionality

# Split the data into training and test sets
X_train = data.iloc[:780]  # 390 samples from each class for training
X_test = data.iloc[780:]  # 10 samples from each class for testing
y_train = labels.iloc[:780]
y_test = labels.iloc[780:]

# Calculate class means
mean_male = X_train[y_train == "male"].mean()
mean_female = X_train[y_train == "female"].mean()

# Compute within-class scatter matrix Sw and between-class scatter matrix Sb
Sw = ((X_train[y_train == "male"] - mean_male).T @ (X_train[y_train == "male"] - mean_male) +
      (X_train[y_train == "female"] - mean_female).T @ (X_train[y_train == "female"] - mean_female))

Sb = ((mean_male - mean_female).values.reshape(-1, 1) @ (mean_male - mean_female).values.reshape(1, -1))

# Calculate eigenvectors and eigenvalues of Sw^(-1) * Sb
eigenvalues, eigenvectors = np.linalg.eigh(np.linalg.inv(Sw) @ Sb)

# Sort eigenvalues and select the top d' eigenvectors
eigenvalue_index = np.argsort(eigenvalues)[::-1]
top_eigenvectors = eigenvectors[:, eigenvalue_index[:d_prime]]

# Project the data onto the reduced dimensional space
X_train_lda = X_train @ top_eigenvectors
X_test_lda = X_test @ top_eigenvectors

# Simple Bayes Classifier
def bayes_classifier(X_train, y_train, X_test):
    classes = np.unique(y_train)
    predictions = []
    
    for x in X_test:
        distances = []
        for c in classes:
            class_mean = X_train[y_train == c].mean(axis=0)
            distance = np.linalg.norm(x - class_mean)
            distances.append((c, distance))
        predicted_class = min(distances, key=lambda x: x[1])[0]
        predictions.append(predicted_class)
    
    return predictions

# Train the Bayes classifier and make predictions
predictions = bayes_classifier(X_train_lda, y_train, X_test_lda)



# Calculate accuracy
accuracy = np.mean(predictions == y_test)
print("Accuracy:", accuracy)
