#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#pip install openai

import os


from openai import OpenAI
client = OpenAI(api_key= "")

def extract_criteria(file_content):
    # Directly use the content from the file as the prompt
    prompt = (
        """
Please extract the following data from the given abstract and present it in a CSV-compatible format. Each value should be separated by a comma, and the columns should be named as follows:

- **Digital Health Technology Used**
- **WHO User Category** (options:
	Person- Persons are members of the public who are potential or current users of health services including patients,
	Provider- Health care providers or providers in training such as medical students are members of the health workforce who deliver health interventions,
	Data Services- Activities related to data management, use, and data governance compliance,
	Health Management- Health management and support personnel are involved in the administration and oversight of health systems)
- **Purpose** (options:
	Education- Providing learning,
	Treatment- The treatment arm in the trial design,
	Participant- Focused directly on participant engaging, screening, recruitment, and retention,
	Assistance- Helping to facilitate the clinical trial as a complement to treatment- typically an administrative component, not a treatment)
- **Health Specialty**  (options: American Medical Association recognized specialties)
- **Trial Registry Number**

If the data element belongs to more than one category, list all that apply using spaces to separate multiple categories instead of commas. For any data not reported in the abstract, return "not reported". Here's the CSV format to use:

DHT Used,DHT User,DHT Purpose,Health Specialty,Trial Number
<Extracted Data>,<Extracted Data>,<Extracted Data>,<Extracted Data>,<Extracted Data>
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
input_directory = ''
output_directory = ''
process_files(input_directory, output_directory)



