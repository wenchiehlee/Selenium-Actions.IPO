import csv
import sys
import json

def count_csv_lines(file_path, output_path, label):
    """
    Counts the number of data lines (excluding header) in a CSV file
    and writes the count to a JSON file in Shields.io format with a custom label.

    Parameters:
        file_path (str): Path to the input CSV file.
        output_path (str): Path to the output JSON file.
        label (str): Label for the badge.
    """
    try:
        # Open the CSV file in read mode with UTF-8 encoding
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            
            # Skip the header line
            next(reader, None)
            
            # Count the lines in the file
            line_count = sum(1 for _ in reader)
        
        # Create a JSON structure compatible with Shields.io
        badge_data = {
            "schemaVersion": 1,
            "label": label,
            "message": str(line_count),
            "color": "blue"
        }

        # Write the badge data to the output JSON file
        with open(output_path, 'w') as json_file:
            json.dump(badge_data, json_file, indent=4)

        print(f"Badge JSON written to '{output_path}'.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Ensure the script is run with exactly three arguments
    if len(sys.argv) != 4:
        print("Usage: python count_csv_lines.py <output_path> <file_path> <label>")
    else:
        output_file = sys.argv[1]
        input_file = sys.argv[2]
        badge_label = sys.argv[3]
        count_csv_lines(input_file, output_file, badge_label)
