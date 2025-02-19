#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
import glob
import os

# Path to the directory containing the files
file_path = ''

# List of files to process
files = glob.glob(os.path.join(file_path, '*.txt_output.txt'))

# Initialize a list to store the data
data = []

# Process each file
for file in files:
    file_name = os.path.basename(file)
    with open(file, 'r') as f:
        content = f.read()
        print(f"Processing file: {file_name}")
        print("Content:", content)
        try:
            # Extract task responses
            task_1_response = content.split('Task 1:')[1].split('Task 2:')[0].strip()
            task_2_response = content.split('Task 2:')[1].split('Task 3:')[0].strip()
            task_3_response = content.split('Task 3:')[1].strip()
            print("Task 1 Response:", task_1_response)
            print("Task 2 Response:", task_2_response)
            print("Task 3 Response:", task_3_response)
            # Append the data to the list
            data.append([file_name, task_1_response, task_2_response, task_3_response])
        except IndexError as e:
            print(f"Error processing file {file_name}: {e}")

# Create a DataFrame
df = pd.DataFrame(data, columns=['File Name', 'Task 1 Response', 'Task 2 Response', 'Task 3 Response'])

# Write the DataFrame to an Excel file
output_file = ''
df.to_excel(output_file, index=False)

print(f"Data has been written to {output_file}")
