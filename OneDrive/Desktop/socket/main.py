import numpy as np
import math

def kl_distance(p, q):
    return np.sum(p * np.log(p / q))

def bhattacharyya_distance(p, q):
    return -np.log(np.sum(np.sqrt(p * q)))

# Define the two histograms H1 and H2
H1 = np.array([0.24, 0.2, 0.16, 0.12, 0.08, 0.04, 0.12, 0.04])
H2 = np.array([0.22, 0.23, 0.16, 0.13, 0.11, 0.08, 0.05, 0.02])

# Calculate KL Distance
kl_distance_result = kl_distance(H1, H2)

# Calculate Bhattacharyya Distance
bhattacharyya_distance_result = bhattacharyya_distance(H1, H2)

# Print the results
print("KL Distance:", kl_distance_result)
print("Bhattacharyya Distance:", bhattacharyya_distance_result)
