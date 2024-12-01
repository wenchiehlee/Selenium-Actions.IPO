#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import sys

def read_file(name, encoding='Big5'):
    try:
        with open(name, 'r', encoding=encoding) as file:
            content = file.read()
            print(content)
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
        sys.stdin.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')
        read_file(filename, encoding)