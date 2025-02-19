#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#pip install openai

from openai import OpenAI
client = OpenAI(api_key= "")

import os

def extract_criteria(file_content):
    # Directly use the content from the file as the prompt
    prompt = (
        """
The input file contains the methods participant eligibility criteria from the methods section of a digital health technology enabled randomized controlled trial (RCT) manuscript.
Your task is to identify any participant inclusion or exclusion criteria related specifically to the use of the digital health technology.

For each file:
1. Extract any **inclusion criteria** directly relating to access, usage, or requirements for the digital health technology.
2. Extract any **exclusion criteria** directly relating to the inability to access, use, or meet requirements for the digital health technology.
3. If no inclusion or exclusion criteria are reported relating to the digital health technology, respond with "not reported".

The output should be formatted as a structured text file that can be easily post-processed into a CSV. Use the following format:

Inclusion Criteria:
<list inclusion criteria here>

Exclusion Criteria:
<list exclusion criteria here>

If multiple criteria exist, list them on separate lines under each category.
If no criteria are reported, write "not reported" under the respective category.

"""

        + file_content
    )

    # Call the OpenAI API with the content of the file
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.25, #0.0
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content

def process_files(input_folder, output_folder):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over each file in the input folder
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)

        # Check if it is a text file
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

                # Extract criteria using the provided function
                result = extract_criteria(content)

                # Define output file path
                output_file_path = os.path.join(output_folder, f"processed_{filename}")

                # Write the result to the output file
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(result)

# Usage
input_directory = ""
output_directory = ""
process_files(input_directory, output_directory)



