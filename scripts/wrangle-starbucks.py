"""
Expects a single filename argument
converts tab delimitation to CSV
cuts out second-line of inkjunk

python scripts/wrangle-starbucks.py \
   data/raw/starbucks_locations.csv \
   > data/wrangled/starbucks_locations.csv
"""

from csv import DictReader, DictWriter
from datetime import date
from re import search
from sys import argv, stdout

HEADERS = ["Store ID","Name","Store Number",
    "Phone Number","Ownership Type","Street Combined",
    "City","Country Subdivision",
    "Country","Postal Code",
    "Latitude","Longitude"]


if __name__ == '__main__':
    srcpath = argv[1]
    wcsv = DictWriter(stdout, fieldnames=HEADERS)
    wcsv.writeheader()
    with open(srcpath, 'r') as rf:
        rcsv = DictReader(rf)
        for row in rcsv:
            wcsv.writerow({k: v.strip() for k, v in row.items() if k in HEADERS})
