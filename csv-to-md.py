#!/usr/bin/python
# -*- coding: UTF-8 -*-
from csv2md.table import Table
import sys

def read_file(name, encoding='Big5'):
    try:
        with open(name, 'r', encoding=encoding) as file:
            table = Table.parse_csv(file,columns=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])
            print(table.markdown())
    except FileNotFoundError:
        print(f"File '{name}' not found.")
    except UnicodeDecodeError:
        print(f"Cannot decode file '{name}' with encoding '{encoding}'.")

if __name__ == "__main__":
    # Check if at least one argument (filename) is provided
    if len(sys.argv) < 2:
        print("Usage: ReadFile.py <filename> [encoding]")
    else:
        filename = sys.argv[1]
        encoding = sys.argv[2] if len(sys.argv) > 2 else 'Big5'
        read_file(filename, encoding)