import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Load the spreadsheet
file_path = 'a few more DHT RCTs_abstracts.xlsx'
df = pd.read_excel(file_path)

# Extract DOI column (Column F)
dois = df.iloc[:, 5].dropna()

# Directory to save abstracts
output_dir = 'abstracts_auto_2'
os.makedirs(output_dir, exist_ok=True)

# Function to fetch abstract from PubMed
def fetch_abstract(doi):
    search_url = f"https://pubmed.ncbi.nlm.nih.gov/?term={doi}"
    response = requests.get(search_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        abstract_section = soup.find('div', {'class': 'abstract-content'})
        if abstract_section:
            return abstract_section.get_text(strip=True)
    return None

# Process each DOI
for doi in dois:
    # Format the DOI for file naming
    file_name = doi.replace('/', '_') + '.txt'
    file_path = os.path.join(output_dir, file_name)

    # Fetch the abstract
    abstract = fetch_abstract(doi)
    if abstract:
        # Save the abstract to a .txt file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(abstract)
        print(f"Saved abstract for DOI: {doi}")
    else:
        print(f"Abstract not found for DOI: {doi}")
