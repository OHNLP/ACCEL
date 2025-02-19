#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#pip install openai
#pip install pymupdf



import os
import fitz

from openai import OpenAI
client = OpenAI(api_key= "")


# Path to the PDF file
pdf_file_path = ""


def extract_text_from_pdf(pdf_path):
    """Extract text from the given PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    return text

def extract_criteria(file_content):
    """Extract participant eligibility criteria related to digital health technology using GPT-4o."""
    prompt = (
        """
The input file contains the methods participant eligibility criteria from the methods section of a digital health technology enabled randomized controlled trial (RCT) manuscript.
Your task is to identify any participant inclusion or exclusion criteria related specifically to the use of the digital health technology.

For each file:
1. Extract any **inclusion criteria** directly relating to access, usage, or requirements for the digital health technology.
2. Extract any **exclusion criteria** directly relating to the inability to access, use, or meet requirements for the digital health technology.
3. If no inclusion or exclusion criteria are reported relating to the digital health technology, respond with "not reported" for both categories.


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
        messages=[{"role": "user", "content": prompt}],
        temperature=0.25,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    print(response.choices[0].message.content)
    return response.choices[0].message.content

# Extract text from the PDF
pdf_text = extract_text_from_pdf(pdf_file_path)

# Process the extracted text
extracted_data = extract_criteria(pdf_text)

# Save the extracted data to a file
output_file_path = ""
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)  # Ensure output folder exists

with open(output_file_path, "w", encoding="utf-8") as output_file:
    output_file.write(extracted_data)

print(f"Processed data saved to {output_file_path}")
