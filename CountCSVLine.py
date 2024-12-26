import csv
import sys
import json

def count_csv_lines(file_path, output_path):
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            line_count = sum(1 for _ in reader)
        
        # Create a Shields.io-compatible JSON
        badge_data = {
            "schemaVersion": 1,
            "label": "Lines",
            "message": str(line_count),
            "color": "blue"
        }

        with open(output_path, 'w') as json_file:
            json.dump(badge_data, json_file, indent=4)
        print(f"Badge JSON written to '{output_path}'.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python count_csv_lines.py <output_path> <file_path>")
    else:
        output_file = sys.argv[1]
        input_file = sys.argv[2]
        count_csv_lines(input_file, output_file)
