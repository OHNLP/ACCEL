import os
import csv


# Define folder path and output CSV file path
folder_path = ""
output_csv = ""

# Define the header line to look for
header_line = "DHT Used,DHT User,DHT Purpose,Health Specialty,Trial Number"

# Prepare a list to store rows
rows = []

# Iterate over all files in the specified folder
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)

    # Process only .txt files
    if file_name.endswith(".txt"):
        with open(file_path, 'r') as file:
            lines = file.readlines()

            # Look for the header line and extract data
            for i, line in enumerate(lines):
                if header_line in line:
                    if i + 1 < len(lines):  # Ensure there's a line below the header
                        data_line = lines[i + 1].strip()
                        data_columns = data_line.split(",")

                        # Add file name and data to rows
                        rows.append([file_name] + data_columns)
                    break

# Write the data to the output CSV file
with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)

    # Write the header row
    writer.writerow(["File Name", "DHT Used", "DHT User", "DHT Purpose", "Health Specialty", "Trial Number"])

    # Write the extracted rows
    writer.writerows(rows)

print(f"Data extraction complete. CSV file saved at: {output_csv}")
