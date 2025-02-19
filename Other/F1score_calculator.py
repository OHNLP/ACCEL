#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score

# File paths
input_file = ''
output_file = ''

# Load the CSV file without headers
data = pd.read_csv(input_file, header=None)

# Assume the first column contains true values and the second column contains predicted values
true_values = data[0]
predicted_values = data[1]

# Calculate confusion matrix components
tn, fp, fn, tp = confusion_matrix(true_values, predicted_values).ravel()

# Calculate metrics
precision = precision_score(true_values, predicted_values)
sensitivity = recall_score(true_values, predicted_values)  # Same as recall
specificity = tn / (tn + fp) if (tn + fp) != 0 else 0
npv = tn / (tn + fn) if (tn + fn) != 0 else 0
f1 = f1_score(true_values, predicted_values)

# Create a dictionary to store the metrics
metrics = {
    'Metric': ['Precision', 'Sensitivity (Recall)', 'Specificity', 'Negative Predictive Value (NPV)', 'F1 Score'],
    'Value': [precision, sensitivity, specificity, npv, f1]
}

# Convert metrics to a DataFrame
metrics_df = pd.DataFrame(metrics)

# Save metrics to the output file
metrics_df.to_csv(output_file, index=False)

print(f"Metrics have been calculated and saved to {output_file}.")