import pandas as pd
import argparse
import sys

def remove_duplicates_keep_newest(input_file, output_file):
    """
    Removes duplicate entries in a CSV file based on stock code (股票代號),
    keeping only the most recent entry according to application date (申請日期).
    
    Args:
        input_file (str): Path to the input CSV file
        output_file (str): Path to save the cleaned CSV file
    """
    try:
        # Load the CSV file
        print(f"Loading file: {input_file}")
        df = pd.read_csv(input_file, encoding='utf-8')
        
        # Display initial information
        print(f"Original dataset: {len(df)} rows")
        
        # Convert 申請日期 to datetime for proper comparison
        # First, check the date format and handle potential format issues
        date_samples = df['申請日期'].head(5).tolist()
        print(f"Date format samples: {date_samples}")
        
        # Try to determine date format (assuming it's consistent)
        try:
            # Attempt to parse the first date to determine format
            sample_date = df['申請日期'].iloc[0]
            if '/' in sample_date:
                # Format like YY/MM/DD or YYYY/MM/DD
                if len(sample_date.split('/')[0]) == 2:
                    df['申請日期'] = pd.to_datetime(df['申請日期'], format='%y/%m/%d', errors='coerce')
                else:
                    df['申請日期'] = pd.to_datetime(df['申請日期'], format='%Y/%m/%d', errors='coerce')
            elif '-' in sample_date:
                # Format like YYYY-MM-DD
                df['申請日期'] = pd.to_datetime(df['申請日期'], format='%Y-%m-%d', errors='coerce')
            else:
                # Try automatic parsing
                df['申請日期'] = pd.to_datetime(df['申請日期'], errors='coerce')
        except:
            print("Could not determine date format. Trying automatic parsing...")
            df['申請日期'] = pd.to_datetime(df['申請日期'], errors='coerce')
        
        # Check for any parsing failures
        if df['申請日期'].isna().any():
            print(f"Warning: {df['申請日期'].isna().sum()} dates could not be parsed.")
        
        # Sort by date (newest first) to prepare for duplicate identification
        df = df.sort_values(by='申請日期', ascending=False)
        
        # Before removing duplicates, identify and print information about them
        duplicates = df[df.duplicated('股票代號', keep=False)].sort_values('股票代號')
        if not duplicates.empty:
            print(f"\nFound {len(duplicates)} rows with duplicate stock codes ({len(duplicates['股票代號'].unique())} unique codes)")
            
            # Group by stock code and analyze each group
            for code, group in duplicates.groupby('股票代號'):
                print(f"\nDuplicate stock code: {code} - {group['公司名稱'].iloc[0]}")
                print(f"Found {len(group)} entries:")
                
                # Sort group by date to identify which will be kept/removed
                sorted_group = group.sort_values('申請日期', ascending=False)
                
                # Print information about each duplicate entry
                for idx, row in sorted_group.iterrows():
                    original_idx = df.index.get_loc(idx) + 1  # +1 for 1-based row numbering
                    status = "KEEP (newest)" if idx == sorted_group.index[0] else "REMOVE (older)"
                    print(f"  Row {original_idx}: Date {row['申請日期'].strftime('%Y-%m-%d')} - {status}")
        else:
            print("No duplicates found based on stock code (股票代號).")
        
        # Remove duplicates, keeping the first occurrence (which is the newest due to our sorting)
        df_no_duplicates = df.drop_duplicates(subset='股票代號', keep='first')
        
        # Count how many were removed
        removed_count = len(df) - len(df_no_duplicates)
        print(f"\nRemoved {removed_count} duplicate entries")
        print(f"Final dataset: {len(df_no_duplicates)} rows")
        
        # Save the clean dataset to a new file
        df_no_duplicates.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Saved clean data to {output_file}")
        
        return True
    
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Remove duplicate stock codes from CSV, keeping the newest entries.')
    parser.add_argument('input_file', help='Path to the input CSV file')
    parser.add_argument('output_file', help='Path to save the cleaned CSV file')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run the duplicate removal function
    success = remove_duplicates_keep_newest(args.input_file, args.output_file)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()