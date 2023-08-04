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
            data.append((layout_element.get_text(), textboxFont, textboxSize))

filtered = []


for x in data:
    if len(x[0]) > 5:
        filtered.append(x)

antragsElement = ["", "", ""]

anträge = []

for x in range(len(filtered)):
    object = filtered[x]
    if object[0].startswith("Titel"):
        if antragsElement != ["","",""]:
            anträge.append(antragsElement)
            antragsElement = ["","",""]
        antragsElement[0] = filtered[x+1][0]
        print(antragsElement)
        continue
    if object[0].startswith("AntragstellerInnen"):
        antragsElement[1] = filtered[x+1][0]
        continue

    if abs(object[2] - 8.96) < 0.1:
        antragsElement[2] += object[0]

print(anträge)
