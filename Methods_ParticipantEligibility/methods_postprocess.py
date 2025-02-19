import os
import csv
import re

def extract_criteria(text):
    # Improved regex patterns to capture varied file formats
    inclusion_patterns = [
        re.compile(r'(?i)Inclusion Criteria:\s*(.*?)(?=\n\n|Exclusion Criteria:|$)', re.DOTALL),
        re.compile(r'(?i)Inclusion:\s*(.*?)(?=\n\n|Exclusion:|$)', re.DOTALL),
        re.compile(r'(?i)Eligible Participants:\s*(.*?)(?=\n\n|Ineligible Participants:|$)', re.DOTALL)
    ]
    exclusion_patterns = [
        re.compile(r'(?i)Exclusion Criteria:\s*(.*?)(?=\n\n|$)', re.DOTALL),
        re.compile(r'(?i)Exclusion:\s*(.*?)(?=\n\n|$)', re.DOTALL),
        re.compile(r'(?i)Ineligible Participants:\s*(.*?)(?=\n\n|$)', re.DOTALL)
    ]
    
    inclusion_criteria = "not reported"
    exclusion_criteria = "not reported"
    
    for pattern in inclusion_patterns:
        match = pattern.search(text)
        if match and match.group(1).strip():
            inclusion_criteria = match.group(1).strip().replace('\n', '; ')
            break
    
    for pattern in exclusion_patterns:
        match = pattern.search(text)
        if match and match.group(1).strip():
            exclusion_criteria = match.group(1).strip().replace('\n', '; ')
            break
    
    return inclusion_criteria, exclusion_criteria

def process_files(input_folder, output_csv):
    data = []
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                text = file.read()
                inclusion, exclusion = extract_criteria(text)
                data.append([filename, inclusion, exclusion])
    
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["File Name", "Inclusion Criteria", "Exclusion Criteria"])
        writer.writerows(data)
    
    print(f"Processing complete. Data saved to {output_csv}")


if __name__ == "__main__":
    input_folder = ""  # Update this path
    output_csv = ""
    process_files(input_folder, output_csv)