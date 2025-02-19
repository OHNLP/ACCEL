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
# %%
for index in range(0,len(onlyfiles)):
    before_intro_text_dict = {}
    abstract_text_dict = {}
    document_title = {}

for index in range(0,len(onlyfiles)):
    path_combine = mypath + "/"+ str(onlyfiles[index])
    import fitz
    doc = fitz.open(path_combine)
    methods_candidate_font_size = 0
    methods_candidate_font_cha = "null"
    methods_candidate_font_bbox = ()
    start_recording_before_intro = True
    start_recording_abstract = False
    keep_recording_abstract = True
    before_intro_text = ""
    abstract_text = ""
    document_title[index]= str(onlyfiles[index])
    for page_n, page in enumerate(doc):
        
        width = page.rect.width
        height = page.rect.height
        if page_n == 1:
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
                            if ("Abstract" in text or "abstract" in text or "ABSTRACT" in text) and (len(text)<35):
                                #print(f"Text: {text}, Font: {font}, Size: {size}, Flags: {flags}")
                                methods_candidate_font_cha = font
                                methods_candidate_font_size = size
                                methods_candidate_font_bbox = block['bbox']
                                start_recording_abstract = True
                            if ("Introduction" in text or "INTRODUCTION" in text or "INTRO" in text or "Intro" in text or "intro" in text or
                                "1.INTRODUCTION" in text or "I n t r o" in text or "I N T R O" in text ) and (len(text)<25):
                                #
                                keep_recording_abstract = False
                            
                            if start_recording_abstract and keep_recording_abstract:
                                abstract_text=abstract_text+""+text
                                #print(f"Text: {abstract_text}, Font: {font}, Size: {size}, Flags: {flags}")
                                
                            if start_recording_before_intro and keep_recording_abstract:
                                before_intro_text=before_intro_text+""+text
        else:
            pass
    #print(f"Text: {before_intro_text}, Font: {font}, Size: {size}, Flags: {flags}")
    
    abstract_text_dict[index]=abstract_text
    before_intro_text_dict[index]=before_intro_text
            
        
doc.close()
# %%
output_dict_list = []
for index in range(0,len(onlyfiles)):
    output_dict = {"Index":index,"Title":document_title[index],"Abstract_(Before_Intro)":before_intro_text_dict[index]}
    output_dict_list.append(output_dict)
output_dict_frame = pd.DataFrame(output_dict_list)
output_dict_frame.to_csv("")

with open('', 'w') as outfile:
    for index in range(0,len(onlyfiles)):
        output_dict = {"Index":index,"Title":document_title[index],"Abstract_(Before_Intro)":before_intro_text_dict[index]}
        json.dump(output_dict, outfile)
        outfile.write('\n')


# %%
    
