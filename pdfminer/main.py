#!/bin/python3

from pathlib import Path
from typing import Iterable, Any

from pdfminer.high_level import extract_pages

pages = extract_pages("small.pdf")

for page_layout in pages:
    
    for x in page_layout:
        print(x)