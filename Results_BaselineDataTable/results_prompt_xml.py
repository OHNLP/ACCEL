#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#pip install openai


import os
import time


from openai import OpenAI
client = OpenAI(api_key= "")


def extract_criteria(file_content):
    prompt = (
        """
        Read the provided XML file for a randomized controlled trial.
        Locate the baseline participant demographics/characteristics table in the results section.
        If the table is not found, return 'Table Not Reported' and do not proceed with analysis.
        If the table is found, evaluate the presence of the following variables: Age, Sex, Race, Education, Income,
        Employment Status, Housing Status, Disability Status, Insurance Status, Internet Access, Gender, Environmental Safety.
        For each variable, return 1 if it is reported in the table, otherwise return 0.
        Output the results in the following JSON format:
        table_reported:
        variables:
        Age:
        Sex:
        Race:
        Education:
        Income:
        Employment Status:
        Housing Status:
        Disability Status:
        Insurance Status:
        Internet Access:
        Gender:
        Environmental Safety:
        """
        + file_content
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.25,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error during API call: {e}"

def count_tokens(text):
    """Estimate the number of tokens in a text string."""
    # A rough estimate assuming ~4 characters per token
    return len(text) // 4

def truncate_to_token_limit(text, token_limit):
    """Truncate the text to fit within the token limit."""
    safe_limit = token_limit - 500  # Adding a safety buffer of 500 tokens
    estimated_tokens = count_tokens(text)
    if estimated_tokens > safe_limit:
        truncation_ratio = safe_limit / estimated_tokens
        truncated_length = int(len(text) * truncation_ratio)
        return text[:truncated_length]
    return text

def process_files(input_folder, output_folder, token_cap=30000, wait_time=90):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if filename.endswith('.xml'):
            print(f"Processing file: {filename}")

            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                file_tokens = count_tokens(content)
                if file_tokens > token_cap:
                    print(f"Truncating {filename} to {token_cap - 500} tokens.")
                    content = truncate_to_token_limit(content, token_cap)

                result = extract_criteria(content)
                print(f"Result for {filename}: {result[:200]}...")  # Debug output

                output_file_path = os.path.join(output_folder, f"processed_{filename}")
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    output_file.write(result)

                print(f"Waiting for {wait_time} seconds to avoid rate limits...")
                time.sleep(wait_time)

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    print("Processing complete.")

# Usage
input_directory = ''
output_directory = ''
process_files(input_directory, output_directory)



