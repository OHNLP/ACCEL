# -*- coding: utf-8 -*-


import csv
from lxml import etree
import pandas as pd
import json
from io import StringIO
import os
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
mypath = ""
#onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
files = os.listdir(mypath)
onlyfiles = [i for i in files if i.endswith('.pdf')]

outputp1 = open('pdf_output.json', 'w',encoding='utf-8')


# %%
for index in range(0,len(onlyfiles)):
    method_text_dict = {}
    document_title = {}

for index in range(0,len(onlyfiles)):
    path_combine = mypath + "/"+ str(onlyfiles[index])
    import fitz
    doc = fitz.open(path_combine)
    methods_candidate_font_size = 0
    methods_candidate_font_cha = "null"
    methods_candidate_font_bbox = ()
    start_recording = False
    keep_recording = True
    method_text = ""
    document_title[index]= str(onlyfiles[index])
    for page_n, page in enumerate(doc):
        
        width = page.rect.width
        height = page.rect.height
        if page_n == 0:
            crop_rectangle = (0, height/100*75, width, height/100*90)
            
                    
            
        else:
            crop_rectangle = (0, 0, width, height)
        rect = fitz.Rect(crop_rectangle)
        
        blocks = page.get_text("dict",clip=rect)["blocks"]
        
        
        
        for block in blocks:
            if block['type'] == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"]
                        font = span["font"]
                        size = span["size"]
                        flags = span["flags"]
                        if ("Methods" in text or "METHODS" in text or "METHOD" in text or "Method" in text) and (len(text)<35):
                            print(f"Text: {text}, Font: {font}, Size: {size}, Flags: {flags}")
                            methods_candidate_font_cha = font
                            methods_candidate_font_size = size
                            methods_candidate_font_bbox = block['bbox']
                            start_recording = True
                        if ("Result" in text or "result" in text or "RESULT" in text) and (len(text)<20) and font==methods_candidate_font_cha and size==methods_candidate_font_size:
                            #print(f"Text: {text}, Font: {font}, Size: {size}, Flags: {flags}")
                            keep_recording = False
                        if ("3.Result" in text or "3.result" in text or "3.RESULT" in text or "3. RESULT" in text or "3. Result" in text or "3. result" in text or "3.  RESULT" in text or "3.  Result" in text or "3.  result" in text):
                                #print(f"Text: {text}, Font: {font}, Size: {size}, Flags: {flags}")
                            keep_recording = False
                        if ("4.Result" in text or "4.result" in text or "4.RESULT" in text or "4. RESULT" in text or "4. Result" in text or "4. result" in text or "4.  RESULT" in text or "4.  Result" in text or "4.  result" in text):
                                #print(f"Text: {text}, Font: {font}, Size: {size}, Flags: {flags}")
                            keep_recording = False
                        if start_recording and keep_recording:
                            method_text=method_text+" "+text
        
        method_text_dict[index]=method_text
        
doc.close()
# %%
output_dict_list = []
for index in range(0,len(onlyfiles)):
    output_dict = {"Index":index,"Title":document_title[index],"Method":method_text_dict[index]}
    output_dict_list.append(output_dict)
output_dict_frame = pd.DataFrame(output_dict_list)
output_dict_frame.to_csv("")

with open('', 'w') as outfile:
    for index in range(0,len(onlyfiles)):
        output_dict = {"Index":index,"Title":document_title[index],"Method":method_text_dict[index]}
        json.dump(output_dict, outfile)
        outfile.write('\n')


# %%
    
