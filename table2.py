import tabula
import os
import pandas as pd
from PyPDF2 import PdfFileReader
from tabula import read_pdf

with open('data.pdf', 'rb') as f:

    infile = PdfFileReader(f)

folder= 'data.pdf'
paths = [infile + fn for fn in os.listdir(f) if fn.endswith('.pdf')]
for path in paths:
    df = tabula.read_pdf(path, encoding = 'UTF-8', pages = 'all', nospreadsheet = True)
    path = path.replace('pdf', 'csv')
    df.to_csv(path, index = True)

df = read_pdf("data.pdf", encoding = "UTF-8")
print(df)
