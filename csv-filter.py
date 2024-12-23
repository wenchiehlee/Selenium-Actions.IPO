#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys
from csvfilter import Processor
import csv

def filter_rows(row):
    # 檢查 row[0] 是否包含指定的年份
    years = ["2025","2024", "2023", "2022", "2021", "2020", "2019","2018"]
    return any(year in row[0] for year in years) 

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
