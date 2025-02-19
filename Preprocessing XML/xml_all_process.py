# -*- coding: utf-8 -*-

import csv
from lxml import etree
import pandas as pd
import json
from io import StringIO
import os
mypath = ""
files = os.listdir(mypath)
onlyfiles = [i for i in files if i.endswith('.xml')]

outputp1 = open('', 'w',encoding='utf-8')
# %%

for each_file in onlyfiles:
    tree = etree.parse(each_file)
    
    t1_caption = ""
    t1_content = []
    methods_content = []
    acknowledgement = ""
    
    ### Table 1 caption
    try:
        r = tree.xpath("//table-wrap[@id='T1' or @id='Table1' or @id='table1' or @id='table-1' or @id='table-1' or @id='tI'] ")
        caption_1 = r[0].xpath(".//caption")
        caption_txt= caption_1[0].xpath(".//p")
        t1_caption = caption_txt[0].text
        
        ### Table 1 content
        df = pd.read_xml(each_file, xpath="//table-wrap[@id='T1']//table[@frame='hsides']//*")
        abc = tree.xpath("//table-wrap[@id='T1']//table[@frame='hsides']//*")
        for item in abc:
            #print(item.text)
            t1_content.append(item.text)
        ###
    except:
        t1_caption = "Table 1 cannot be crawled at this moment"
    
    ### Methods - methods
    try:
        methods = tree.xpath("//title[contains(text(),'ethods')]")[0].xpath("following-sibling::*")
        for item in methods:
            methods_content.append(str(item.xpath(".//text()")))
            #print()
    except:
        methods_content.append("Methods cannot be crawled at this moment")
    
    #methods = tree.xpath(each_file, xpath="//title/following-sibling::p")
    try:
    ### Acknowledgement
        r2 = tree.xpath("//ack")
        caption_txt= r2[0].xpath(".//p")
        acknowledgement = caption_txt[0].text
    except:
        acknowledgement = "Acknowledgement cannot be crawled at this moment"
    """
    for item in caption_txt:
        print(item.text)
    """
    
    ###
    
    this_dict = {"PMC":each_file,"T1_caption":t1_caption,"T1_content":t1_content,"methods_content":methods_content,"acknowledgement":acknowledgement}
    outputp1.write(json.dumps(this_dict))
    outputp1.write('\n')
    
outputp1.close()
    
