"""
Expects a single filename argument
converts tab delimitation to CSV
cuts out second-line of inkjunk

python scripts/wrangle-atf.py \
   data/raw/atf_firearm_dealers_2016_08.txt \
   > data/wrangled/atf_firearm_dealers_2016_08.csv
"""

import csv
from datetime import date
from re import search
from sys import argv, stdout

if __name__ == '__main__':
    srcpath = argv[1]
    wcsv = csv.writer(stdout)
    with open(srcpath, 'r') as rf:
        rcsv = csv.reader(rf, delimiter='\t')
        wcsv.writerow(next(rcsv)) # write header
        next(rcsv) # skip second line of non-data
        for row in rcsv:
            values = [v.strip() for v in row]
            if values[0]: # skip blank lines
                # last field is the `Expire Date` field
                # which we want to convert to YYYY-MM-DD format
                dt = search(r'(\d{1,2})/(\d{1,2})/(\d{4})', values[-1])
                if dt:
                    month, day, year = [int(d) for d in dt.groups()]
                    values[-1] = date(year, month, day).isoformat()
                wcsv.writerow(values)

