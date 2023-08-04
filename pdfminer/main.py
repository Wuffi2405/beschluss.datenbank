#!/bin/python3

from pathlib import Path
from typing import Iterable, Any

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBox, LTTextLine, LTChar, LTAnno


pages = extract_pages("small.pdf")

data = []

for page_layout in pages:
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
            data.append((layout_element.get_text().strip(), textboxFont, textboxSize))

rml = []
for i, d in enumerate(data):
    if d[0].isdigit():
        rml.append(i)

for i in reversed(rml):
    data.pop(i)



data.sort(key=lambda x: x[2])

for d in reversed(data):
    if len(d[0]) < 3:
        print("ID: " + d[0])
        break

for d in reversed(data):
    if len(d[0]) > 8:
        print("Title: " + d[0])
        break

sorted_fontsize = {}
for d in data:
    if round(d[2], 1) not in sorted_fontsize:
        sorted_fontsize[round(d[2], 1)] = d[0]
    else:
        sorted_fontsize[round(d[2], 1)] += d[0]

most_common_fontsize = None
most_common_fontsize_count = 0
for k, v in sorted_fontsize.items():
    if len(v) > most_common_fontsize_count:
        most_common_fontsize_count = len(v)
        most_common_fontsize = k
print("Content: ", sorted_fontsize[most_common_fontsize])