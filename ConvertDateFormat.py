import pandas as pd
import sys

def convert_and_fix_csv(input_file, output_file):
    """
    Converts specified date columns to 'YYYY/MM/DD' format and ensures all cells
    in the output CSV are wrapped in double quotes.
    """
    # Columns with date data
    date_columns = [
        "申請日期",
        "上櫃審議委員會審議日期",
        "櫃買董事會通過上櫃日期",
        "櫃買同意上櫃契約日期或證期局核准上櫃契約日期",
        "股票上櫃買賣日期"
    ]
    
    try:
        # Read the input CSV file with quotation wrapping preserved
        df = pd.read_csv(input_file, encoding="utf-8", quotechar='"', dtype=str)
        
        # Convert date columns to 'YYYY/MM/DD' format
        for column in date_columns:
            if column in df.columns:
                df[column] = df[column].apply(
                    lambda x: f"{x[:4]}/{x[4:6]}/{x[6:8]}" if pd.notna(x) and len(str(x)) == 8 else x
                )
        
        # Save the modified DataFrame to the output file with all cells quoted
        df.to_csv(output_file, index=False, encoding="utf-8", quoting=1)  # quoting=1 wraps all cells in quotes
        print(f"File successfully processed and saved to: {output_file}")
    
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    # Check if the correct number of arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python ConvertDateFormat.py <input_file> <output_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        convert_and_fix_csv(input_file, output_file)
