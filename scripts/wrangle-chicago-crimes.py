"""
Expects a single filename argument
converts tab delimitation to CSV
cuts out second-line of inkjunk

python scripts/wrangle-chicago-crimes.py \
   data/raw/chicago_homicides_and_gun_crimes.csv \
   > data/wrangled/chicago_homicides_and_gun_crimes.csv
"""

from csv import DictReader, DictWriter
from datetime import datetime
from sys import argv, stdout

HEADERS = ["ID", "Date", "Block", "Primary Type", "Description", "Location Description",
    "Arrest", "Domestic", "Beat", "District", "Latitude", "Longitude"]


if __name__ == '__main__':
    srcpath = argv[1]
    wcsv = DictWriter(stdout, fieldnames=HEADERS)
    wcsv.writeheader()
    with open(srcpath, 'r') as rf:
        rcsv = DictReader(rf)
        for row in rcsv:
            row['Date'] = datetime.strptime(row['Date'], '%m/%d/%Y %I:%M:%S %p').strftime("%Y-%m-%d %H:%M:%S")
            wcsv.writerow({k: v.strip() for k, v in row.items() if k in HEADERS})
