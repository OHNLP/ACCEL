#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#pip install openai

from openai import OpenAI
client = OpenAI(api_key= "")


import os

# Define paths
input_folder = ''  # Folder containing input text files
output_folder = ''  # Folder to save output text files

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define the prompt for sectionalization
prompt_template = (
    "You are a helpful assistant. Take the following text containing the methods "
    "section of a published randomized controlled trial article and extract only the section "
    "containing participant eligibility criteria. Include the entire paragraph relating to both participant inclusion and exclusion criteria. "
    "Do not summarize or paraphrase the criteria. Return the inclusion and exclusion criteria exactly as written in the text..\n\n"
    "Text: '''\n{}\n'''"
)


def extract_criteria(text):
    # Create the prompt with the input text
    prompt = prompt_template.format(text)

    # Call the OpenAI API with the updated format
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.25,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={"type": "text"}
    )

    # Print the response text directly to the console
    print(response.choices[0].message.content)
    return response.choices[0].message.content

# Iterate over each file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        input_file_path = os.path.join(input_folder, filename)
        output_file_path = os.path.join(output_folder, f"parsed_{filename}")

        # Read the input file
        with open(input_file_path, 'r') as file:
            input_text = file.read()

        # Extract the inclusion and exclusion criteria
        parsed_text = extract_criteria(input_text)

        # Write the parsed text to the output file
        with open(output_file_path, 'w') as file:
            file.write(parsed_text)

        print(f"Processed {filename} and saved the parsed section to {output_file_path}")

print("All files have been processed.")
