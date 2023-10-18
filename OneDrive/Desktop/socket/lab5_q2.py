import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from google.colab import drive
drive.mount('/content/drive')

path='/content/drive/MyDrive/doc1.txt'
df1=open(path,"r")
df1

file1=df1.read()
file1

path='/content/drive/MyDrive/doc2.txt'
df2=open(path,"r")
df2

file2=df2.read()
file2

vectorizer = CountVectorizer()
X = vectorizer.fit_transform([file1])
arr1 = X.toarray()
arr1=arr1.T
print(arr1)

vectorizer = CountVectorizer()
X = vectorizer.fit_transform([file2])
arr2 = X.toarray()
print(arr2)

import math

# Calculate the dot product of the two vectors
dot_product = sum([x * y for x, y in zip(arr1, arr2)])
dot_product = np.linalg.norm(dot_product)
# Calculate the magnitude (Euclidean norm) of each vector
magnitude1 = math.sqrt(sum([x**2 for x in arr1]))
magnitude2 = math.sqrt(sum([x**2 for x in arr2.T]))

# Calculate the cosine similarity
cosine_similarity = dot_product / (magnitude1 * magnitude2)

print("Cosine Similarity:", cosine_similarity)