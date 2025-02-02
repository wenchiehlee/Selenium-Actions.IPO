# Instructions for Generating `TWSE-company.py`

1. Extract the Python code used to generate the file `TWSE-company-utf8.csv` from the project files.
2. Ensure the Python code is readable and properly formatted.
3. Use the input CSV file named `applylisting.csv`, which contains metadata at the beginning and end of the file. Remove this metadata before processing. The file is encoded in Big5.
4. The `applylisting.csv` file includes the following columns: 
   - 索引
   - 公司代號
   - 公司簡稱
   - 申請日期
   - 董事長
   - 申請時股本(仟元)
   - 上市審議委員會審議日期
   - 交易所董事會通過上市日期
   - 上市契約報請主管機關備查(主管機關核准)日期
   - 股票上市買賣日期
   - 承銷商
   - 承銷價
   - 備註
5. The UTF-8 encoded version of `applylisting.csv` is named `applylisting-utf8.csv`.
6. The output file is named `TWSE-company-utf8.csv`, containing the following columns in order: 
   - 申請日期
   - 股票代號
   - 公司名稱
   - 董事長
   - 申請時股本(仟元)
   - 上櫃審議委員會審議日期
   - 櫃買董事會通過上櫃日期
   - 櫃買同意上櫃契約日期或證期局核准上櫃契約日期
   - 股票上櫃買賣日期
   - 主辦承銷商
   - 承銷價
   - 備註
7. Include an option to specify whether or not the CSV header should be written to `TWSE-company-utf8.csv`.
8. Map the column 主辦承銷商 in `TWSE-company-utf8.csv` to the column 承銷商 from `applylisting.csv`.
9. Convert all date fields from the Taiwanese calendar (ROC year) format (e.g., `YYY/MM/DD`) to the Gregorian calendar format (e.g., `YYYYMMDD`). The applicable date fields are: 
   - 申請日期
   - 上櫃審議委員會審議日期
   - 櫃買董事會通過上櫃日期
   - 櫃買同意上櫃契約日期或證期局核准上櫃契約日期
   - 股票上櫃買賣日期
10. Remove commas from numerical fields for consistent formatting and processing. The applicable fields are: 
    - 申請時股本(仟元)
    - 承銷價
11. If a date cannot be converted (e.g., due to an invalid format), log the error with sufficient details for debugging.
