import csv
from datetime import datetime
import chardet

# Helper functions
def clean_numeric_field(num_str):
    """Cleans numeric fields by removing commas and quotes."""
    if not num_str or num_str.strip() == "":
        return ""
    return num_str.strip().replace('"', '').replace(',', '')

def convert_date(roc_date):
    """Converts ROC date to Gregorian date in YYYYMMDD format."""
    if not roc_date or roc_date.strip() == "":
        return ""
    try:
        parts = roc_date.strip().split('/')
        if len(parts) == 3:
            year = int(parts[0]) + 1911
            month = int(parts[1])
            day = int(parts[2])
            return datetime(year, month, day).strftime('%Y%m%d')
        else:
            raise ValueError(f"Invalid date format: {roc_date}")
    except Exception as e:
        print(f"Error converting date '{roc_date}': {e}")
        return ""

# Detect encoding of the input file
def detect_encoding(file_path):
    """Detects the encoding of a file."""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

# Main processing function
def process_file(input_file, output_file, write_header=True):
    encoding = detect_encoding(input_file) or 'big5'
    print(f"Detected file encoding: {encoding}")

    with open(input_file, encoding=encoding, errors='replace') as infile, open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write header if enabled
        if write_header:
            writer.writerow([
                "申請日期", "股票代號", "公司名稱", "董事長", "申請時股本",
                "上櫃審議委員會審議日期", "櫃買董事會通過上櫃日期", "櫃買同意上櫃契約日期或證期局核准上櫃契約日期",
                "股票上櫃買賣日期", "主辦承銷商", "承銷價", "備註"
            ])

        for line_number, row in enumerate(reader):
            # Skip metadata, empty rows, or rows with invalid length
            if line_number == 0 or len(row) < 13:
                continue  # Skip header and invalid rows

            # Skip rows where the date fields contain headers or non-date strings
            if row[3].startswith("申請日期"):
                print(f"Skipping header row: {row}")
                continue

            try:
                # Process and clean each field
                cleaned_row = [
                    convert_date(row[3]),  # 申請日期
                    row[1].strip(),  # 股票代號
                    row[2].strip(),  # 公司名稱
                    row[4].strip(),  # 董事長
                    clean_numeric_field(row[5]),  # 申請時股本
                    convert_date(row[6]),  # 上市審議日期
                    convert_date(row[7]),  # 交易所董事會通過日期
                    convert_date(row[8]),  # 契約核准日期
                    convert_date(row[9]),  # 股票上市日期
                    row[10].strip().replace('"', ''),  # 主辦承銷商
                    clean_numeric_field(row[11]),  # 承銷價
                    row[12].strip() if len(row) > 12 else ""  # 備註
                ]

                # Write to output
                writer.writerow(cleaned_row)
            except Exception as e:
                print(f"Error processing line {line_number + 1}: {e}")

if __name__ == "__main__":
    input_file = "applylisting.csv"
    output_file = "TWSE-company-utf8.csv"
    process_file(input_file, output_file, write_header=True)
