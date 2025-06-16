import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Path to the CSV data file
data_path = 'q2.csv'

# Read the CSV data into a DataFrame
data_frame = pd.read_csv(data_path)
df = pd.DataFrame(data_frame)

# Function to calculate the correlation coefficient between two arrays X and Y
def calculate_correlation_coefficient(X, Y):
    n = len(X)
    mean_X = sum(X) / n
    mean_Y = sum(Y) / n
    deviations_X = [x - mean_X for x in X]
    deviations_Y = [y - mean_Y for y in Y]
    sum_of_products = sum([dev_X * dev_Y for dev_X, dev_Y in zip(deviations_X, deviations_Y)])
    sum_of_squares_X = sum([dev_X ** 2 for dev_X in deviations_X])
    sum_of_squares_Y = sum([dev_Y ** 2 for dev_Y in deviations_Y])
    corr_coefficient = sum_of_products / (np.sqrt(sum_of_squares_X) * np.sqrt(sum_of_squares_Y))
    return corr_coefficient

# Extract test scores as a numpy array
test_scores = df['Test Score'].values
test_scores = np.array(test_scores)

# Get the variable names/columns (excluding 'Test Score')
variable_names = df.columns.tolist()
variable_names.remove('Test Score')

# List to store correlation coefficients
correlation_coefficients = []

# Calculate correlation coefficients for each variable
for var_name in variable_names:
    variable_data = df[var_name].values
    variable_data = np.array(variable_data)
    correlation_coefficient = calculate_correlation_coefficient(variable_data, test_scores)
    correlation_coefficients.append(correlation_coefficient)

# Labels for variables
variable_labels = ['Hours Studied', 'Hours Watching TV', 'Outdoor Activity Time', 'Hours Listening to Music', 'Water Consumed']

# Iterate through variables and print results
for i in range(len(variable_labels)):
    correlation = correlation_coefficients[i]
    if correlation > 0:
        connection_message = "{} and Test score are positively connected"
    elif correlation < 0:
        connection_message = "{} and Test score are negatively connected"
    print(connection_message.format(variable_labels[i]))
    print("Correlation coefficient between them is:", correlation)
    print('\n')
