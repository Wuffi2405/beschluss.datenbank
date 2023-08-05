#!/bin/python3

from pathlib import Path
from typing import Iterable, Any

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter

from pdfminer.converter import HTMLConverter
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox, LTTextLine, LTChar, LTAnno, LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO

import json

import os

from os import listdir
from os.path import isdir, isfile
from glob import glob



def extract_file(indir, outdir):

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    data = []
    pages = extract_pages(indir)
    for page_layout in pages:
        print(page_layout)
        for layout_element in page_layout:
            if isinstance(layout_element, LTTextBox):            
                textboxFont = None
                textboxSize = None
                for line_element in layout_element._objs:                
                    if isinstance(line_element, LTTextLine):
                        for character in line_element._objs:
                            if isinstance(character, LTChar):
                                if textboxFont == None:
                                    textboxFont = character.fontname
                                if textboxSize == None:
                                    textboxSize = character.size
                                if textboxFont != character.fontname:
                                    if not character.fontname.endswith("Italic"):
                                        print("MISMATCH", textboxFont, character.fontname)
                                        #exit()
                                if abs(textboxSize - character.size) > 0.01:
                                    print("MISMATCH", textboxSize, character.size)
                                    #exit()
                    else:
                        print("PLEASE HANDLE UNKNOWN ELEMENT: ", line_element)
                        exit()
                data.append((layout_element.get_text(), textboxFont, round(textboxSize,2), layout_element.bbox))

    font_map = {}

    for x in data:
        font_data = (x[1], x[2])
        weight = len(x[0])

        if font_data not in font_map:
            font_map[font_data] = weight
        else:
            font_map[font_data] += weight

    content_data = max(font_map.items(), key = lambda x : x[1])[0]

    probably_content = [x for x in font_map if abs(x[1] - content_data[1]) < 0.1]

    beschlüsse = []

    beschluss_element = ["", ""]

    for x in range(len(data)):
        if (data[x][1], data[x][2]) not in probably_content:
            if "Titel" in data[x][0]:
                if (data[x+1][1], data[x+1][2]) not in probably_content:
                    if beschluss_element != ["",""]:
                        beschlüsse.append(beschluss_element)
                        beschluss_element = ["",""]
                    beschluss_element[0] = data[x+1][0].replace("\n"," ").strip()
        if (data[x][1], data[x][2]) in probably_content:
            if beschluss_element[0] != "":
                if not data[x][0].strip().isdigit():
                    html_data = data[x][0].replace("-\n", "").replace("\n", " ").strip()
                    html_data.replace("\n", " ")
                    html_data.strip()
                    html_data = "<p>" + html_data + "</p>"
                    beschluss_element[1] += html_data

    if beschluss_element != ["",""]:
        beschlüsse.append(beschluss_element)

    for id,e in enumerate(beschlüsse):
        with open(outdir + "/\""+ e[0] + ".json\"", "w") as file:
            file.write(json.dumps({"title": e[0], "text_html": e[1]}, ensure_ascii=False))

    # TODO Add Antragssteller, PDF_document, ID to json

def extract_recursive(indir, outdir):
    for x in listdir(indir):
        if isdir(indir + "/" + x):
            extract_recursive(indir + "/" + x, outdir + "/" + x)
        if isfile(indir + "/" + x):
            if x.endswith(".pdf"):
                foldername = x[:-4]
                print("Found pdf:" , indir + "/" + x)
                print("Extracting to ", outdir + "/" + foldername)
                extract_file(indir + "/" + x, outdir + "/" + foldername)

#extract_recursive(raw_data_dir, data_dir)

raw_data_dir = "../raw_data"
data_dir = "../data"


for x in glob("../raw_data/**/*.pdf"):
    print(x)