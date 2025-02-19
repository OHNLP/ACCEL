#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##############################################     STEP 1     ##############################################
####For multiple files in folder###


import os
from pdf2image import convert_from_path


def convert_pdf(pdf_path, save_dir, res=400):
  """Converts a PDF file to images and saves them in the specified directory.

  Args:
      pdf_path: Path to the PDF file.
      save_dir: Directory to save the converted images.
      res (optional): Resolution of the converted images (default 400 dpi).
  """

  pages = convert_from_path(pdf_path, res)

  name_with_extension = pdf_path.rsplit('/')[-1]
  name = name_with_extension.rsplit('.')[0]

  for idx, page in enumerate(pages):
    page.save(f'{save_dir}/{name}_{idx}.png', "PNG")


def convert_pdfs_in_folder(folder_path, save_dir, res=400):
  """Converts all PDF files in a folder to images and saves them in the specified directory.

  Args:
      folder_path: Path to the folder containing PDF files.
      save_dir: Directory to save the converted images.
      res (optional): Resolution of the converted images (default 400 dpi).
  """

  for filename in os.listdir(folder_path):
    if filename.endswith('.pdf'):
      pdf_file = os.path.join(folder_path, filename)
      convert_pdf(pdf_file, save_dir, res)


if __name__ == "__main__":
  # Update these paths according to your file structure
  pdf_folder = ""
  output_folder = ""
  convert_pdfs_in_folder(pdf_folder, output_folder)

print("All files complete")





##############################################     STEP 2     ##############################################

### read in PNG files and identify tables, if contains a table save in new folderas png and txt

import shutil
import pytesseract
from pytesseract import Output
from PIL import Image

image_folder = ""
destination_folder = ""   # Create this folder if it doesn't exist


# Ensure the destination folder exists
os.makedirs(destination_folder, exist_ok=True)


# Function to check if a table is present in the image using pytesseract
def is_table_present(image_path):
  img = Image.open(image_path)
  d = pytesseract.image_to_data(img, output_type=Output.DICT)

  for word in d['text']:
    if word.lower() in ['table', 'rows', 'columns']:
      return True
  return False


# Process image files
for filename in os.listdir(image_folder):
  if filename.endswith(".png"):
    filepath = os.path.join(image_folder, filename)

    # Try to extract tables from the image
    try:
      if is_table_present(filepath):
        shutil.copy(filepath, os.path.join(destination_folder, filename))

        # Convert the image to text and save as a .txt file
        img = Image.open(filepath)
        text = pytesseract.image_to_string(img)
        txt_filename = os.path.splitext(filename)[0] + ".txt"
        txt_filepath = os.path.join(destination_folder, txt_filename)
        with open(txt_filepath, "w") as txt_file:
          txt_file.write(text)
    except Exception as e:
      print(f"Error processing {filename}: {e}")

print("All files complete")





