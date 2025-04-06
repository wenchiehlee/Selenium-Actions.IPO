import pandas as pd
import argparse
import sys
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import os
import io

# GitHub URL for auction data
GITHUB_AUCTION_URL = "https://raw.githubusercontent.com/wenchiehlee/Selenium-Actions.Auction/refs/heads/main/auction-company.csv"

def download_auction_data(url=GITHUB_AUCTION_URL, local_file=None):
    """
    Download the auction data from GitHub and return as a DataFrame.
    Optionally save to a local file.
    
    Args:
        url (str): URL to download the auction data from
        local_file (str, optional): Path to save the downloaded file
        
    Returns:
        pandas.DataFrame: The downloaded auction data
    """
    try:
        print(f"Downloading auction data from {url}...")
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Save to local file if requested
        if local_file:
            with open(local_file, 'wb') as f:
                f.write(response.content)
            print(f"Saved auction data to {local_file}")
        
        # Return as DataFrame
        return pd.read_csv(io.StringIO(response.content.decode('utf-8')))
    
    except Exception as e:
        print(f"Error downloading auction data: {e}")
        return None

def process_files(ipo_file, output_file, local_auction_file=None):
    """
    Process IPO and auction files to remove duplicate stock codes based on complex rules.
    
    Args:
        ipo_file (str): Path to the IPO CSV file (TWSE_TPEX-IPO-utf8-filter-sort.csv)
        output_file (str): Path to save the cleaned CSV file
        local_auction_file (str, optional): Path to save downloaded auction file
    """
    try:
        # Load the IPO CSV file
        print(f"Loading IPO file: {ipo_file}")
        df_ipo = pd.read_csv(ipo_file, encoding='utf-8')
        print(f"Original IPO dataset: {len(df_ipo)} rows")
        
        # Download and load the auction data
        df_auction = download_auction_data(local_file=local_auction_file)
        if df_auction is None:
            print("Failed to download auction data. Exiting.")
            return False
        
        print(f"Auction dataset: {len(df_auction)} rows")
        
        # Convert date columns to datetime for proper comparison
        convert_dates(df_ipo, '申請日期')
        convert_dates(df_auction, '開標日期')
        
        # Find duplicates in the IPO file
        duplicates = df_ipo[df_ipo.duplicated('股票代號', keep=False)].sort_values('股票代號')
        
        if not duplicates.empty:
            print(f"\nFound {len(duplicates)} rows with duplicate stock codes ({len(duplicates['股票代號'].unique())} unique codes)")
            
            # Create a copy of the original IPO dataframe to mark which rows to keep
            df_ipo['keep_row'] = True
            
            # Process each duplicate group
            for code, group in duplicates.groupby('股票代號'):
                print(f"\nProcessing duplicate stock code: {code} - {group['公司名稱'].iloc[0]}")
                
                # Check if this stock code exists in the auction file
                auction_entries = df_auction[df_auction['股票代號'] == code]
                
                if len(auction_entries) > 0:
                    print(f"  Found {len(auction_entries)} matching entries in the auction file")
                    
                    # Find the row to keep based on the complex rule
                    rows_to_process = []
                    
                    for ipo_idx, ipo_row in group.iterrows():
                        ipo_date = ipo_row['申請日期']
                        
                        # Check each auction entry
                        for auction_idx, auction_row in auction_entries.iterrows():
                            auction_date = auction_row['開標日期']
                            
                            # Check if auction date is after IPO application date
                            if auction_date > ipo_date:
                                # Check if difference is within 12 months
                                diff = relativedelta(auction_date, ipo_date)
                                months_diff = diff.years * 12 + diff.months
                                
                                if months_diff <= 12:
                                    status = "KEEP (auction date within 12 months after application)"
                                    rows_to_process.append((ipo_idx, True, ipo_date, auction_date, months_diff, status))
                                else:
                                    status = "REMOVE (auction date more than 12 months after application)"
                                    rows_to_process.append((ipo_idx, False, ipo_date, auction_date, months_diff, status))
                            else:
                                status = "REMOVE (auction date before application date)"
                                rows_to_process.append((ipo_idx, False, ipo_date, auction_date, None, status))
                    
                    # If we have valid entries to keep
                    if any(keep for _, keep, _, _, _, _ in rows_to_process):
                        # Mark all rows in this group for removal first
                        for idx in group.index:
                            df_ipo.loc[idx, 'keep_row'] = False
                        
                        # Then mark the ones we want to keep
                        for idx, keep, ipo_date, auction_date, months_diff, status in rows_to_process:
                            if keep:
                                df_ipo.loc[idx, 'keep_row'] = True
                                print(f"  Row {df_ipo.index.get_loc(idx) + 1}: Application Date: {ipo_date.strftime('%Y-%m-%d')}, "
                                      f"Auction Date: {auction_date.strftime('%Y-%m-%d')}, "
                                      f"Difference: {months_diff} months - {status}")
                            else:
                                print(f"  Row {df_ipo.index.get_loc(idx) + 1}: Application Date: {ipo_date.strftime('%Y-%m-%d')}, "
                                      f"Auction Date: {auction_date.strftime('%Y-%m-%d')}, "
                                      f"{status}")
                    else:
                        print("  No entries match the criteria. Using default duplicate removal (keeping newest).")
                        # Use default behavior: keep newest application
                        newest_idx = group['申請日期'].idxmax()
                        
                        for idx in group.index:
                            if idx != newest_idx:
                                df_ipo.loc[idx, 'keep_row'] = False
                                print(f"  Row {df_ipo.index.get_loc(idx) + 1}: REMOVE (older application)")
                            else:
                                print(f"  Row {df_ipo.index.get_loc(idx) + 1}: KEEP (newest application)")
                else:
                    print("  No matching entries in the auction file. Using default duplicate removal (keeping newest).")
                    # Use default behavior: keep newest application
                    newest_idx = group['申請日期'].idxmax()
                    
                    for idx in group.index:
                        if idx != newest_idx:
                            df_ipo.loc[idx, 'keep_row'] = False
                            print(f"  Row {df_ipo.index.get_loc(idx) + 1}: REMOVE (older application)")
                        else:
                            print(f"  Row {df_ipo.index.get_loc(idx) + 1}: KEEP (newest application)")
            
            # Filter the dataframe to keep only the rows we want
            df_ipo_cleaned = df_ipo[df_ipo['keep_row']].drop(columns=['keep_row'])
            
            # Count how many were removed
            removed_count = len(df_ipo) - len(df_ipo_cleaned)
            print(f"\nRemoved {removed_count} duplicate entries")
            print(f"Final dataset: {len(df_ipo_cleaned)} rows")
            
            # Save the clean dataset to a new file
            df_ipo_cleaned.to_csv(output_file, index=False, encoding='utf-8')
            print(f"Saved clean data to {output_file}")
        else:
            print("No duplicates found based on stock code (股票代號).")
            # Just save the original file
            df_ipo.to_csv(output_file, index=False, encoding='utf-8')
            print(f"Saved data to {output_file}")
        
        return True
    
    except Exception as e:
        print(f"Error: {e}")
        return False

def convert_dates(df, date_column):
    """
    Converts a date column in a dataframe to datetime format.
    
    Args:
        df (pandas.DataFrame): The dataframe containing the date column
        date_column (str): The name of the date column to convert
    """
    try:
        # Get sample date for format detection
        date_samples = df[date_column].head(5).tolist()
        print(f"{date_column} format samples: {date_samples}")
        
        # Try to determine date format (assuming it's consistent)
        sample_date = df[date_column].iloc[0]
        if '/' in sample_date:
            # Format like YY/MM/DD or YYYY/MM/DD
            if len(sample_date.split('/')[0]) == 2:
                df[date_column] = pd.to_datetime(df[date_column], format='%y/%m/%d', errors='coerce')
            else:
                df[date_column] = pd.to_datetime(df[date_column], format='%Y/%m/%d', errors='coerce')
        elif '-' in sample_date:
            # Format like YYYY-MM-DD
            df[date_column] = pd.to_datetime(df[date_column], format='%Y-%m-%d', errors='coerce')
        else:
            # Try automatic parsing
            df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    
    except Exception as e:
        print(f"Error determining date format for {date_column}, trying automatic parsing: {e}")
        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    
    # Check for any parsing failures
    if df[date_column].isna().any():
        print(f"Warning: {df[date_column].isna().sum()} dates in {date_column} could not be parsed.")

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Remove duplicate stock codes based on IPO and auction data.')
    parser.add_argument('ipo_file', help='Path to the IPO CSV file (TWSE_TPEX-IPO-utf8-filter-sort.csv)')
    parser.add_argument('output_file', help='Path to save the cleaned CSV file')
    parser.add_argument('--save-auction', help='Optional path to save the downloaded auction file', default=None)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run the processing function
    success = process_files(args.ipo_file, args.output_file, args.save_auction)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()