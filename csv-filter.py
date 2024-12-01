#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
from csvfilter import Processor
import csv

def filter_rows(row):
    #print(f"'{row[0]}'")
    return "2024" in row[0] and row[6] != ""

# Set up processor with fields to match the expected number of columns in the CSV
processor = Processor(fields=list(range(26)))  # Fields 0 to 25
processor.add_validator(filter_rows)

# Modify the output stream to avoid additional newlines
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(newline='')

# Set up CSV writer for standard output, with all items quoted
writer = csv.writer(sys.stdout, quotechar='"', quoting=csv.QUOTE_ALL)

# Write header row to standard output
writer.writerow(["申請日期", "股票代號", "公司名稱", "董事長", "申請時股本", "上櫃審議委員會審議日期", "櫃買董事會通過上櫃日期", "櫃買同意上櫃契約日期或證期局核准上櫃契約日期", "股票上櫃買賣日期", "主辦承銷商", "承銷價", "備註"])

# Process rows and write each filtered row to standard output
for filtered_row in processor.process(sys.stdin):
    writer.writerow(filtered_row)
