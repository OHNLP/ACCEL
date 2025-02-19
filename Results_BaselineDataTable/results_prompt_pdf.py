#!/usr/bin/env python3
# -*- coding: utf-8 -*-



#pip install OpenAI

import os
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key="")

# Define folder paths
folder_path = ""
output_folder_path = ""

# Ensure output folder exists
os.makedirs(output_folder_path, exist_ok=True)

# Function to check if the file is valid for processing
def is_valid_file(file_name):
    """Check if the file is valid for processing."""
    return not file_name.startswith('.DS_Store')

# Function to process each file
def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Task 1: The input file is from a published randomized controlled trial. Does the file contain a table in true row and column format? If the file contains a true table respond yes. If there is not a true table, respond no. Task 2: Does the table contain baseline participant demographics and characteristics data? If the file contains a baseline participant demographics table, respond with yes. If the table does not contain baseline demographic details, respond with no. Only evaluate tables for baseline demographic details, not summaries or descriptions of such tables. Task 3: Conduct a binary evaluation of the reported table variables Age, Sex, Race, Education, Income, Employment Status, Housing Status, Disability Status, Insurance Status, Internet Access, Gender, Environmental Safety. If only male or female is reported without specifying sex or gender, classify this in the gender category. Write 1 if the variable is reported or 0 if the variable is not reported. The final response should consist of only the following: Task 1 yes or no; Task 2 yes or no; and Task 3 the 12 binary reporting scores."

                },
                {
                    "role": "user",
                    "content": content
                }
            ],
            temperature=0.25,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        response_message = response.choices[0].message.content
        return response_message
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError processing file {file_path}: {e}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    return None

# Iterate through files in the folder
for filename in os.listdir(folder_path):
    if is_valid_file(filename):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            try:
                result = process_file(file_path)

                if result is not None:
                    # Save the result to the output folder
                    output_file_path = os.path.join(output_folder_path, f"{filename}_output.txt")
                    with open(output_file_path, 'w') as output_file:
                        output_file.write(result)
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

print("Processing complete.")