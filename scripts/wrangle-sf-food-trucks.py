"""
Expects a single filename argument
converts tab delimitation to CSV
cuts out second-line of inkjunk

python scripts/wrangle-sf-food-trucks.py \
   data/raw/sf_food_trucks.csv > data/wrangled/sf_food_trucks.csv
"""

from csv import DictReader, DictWriter
from datetime import datetime
from sys import argv, stdout

HEADERS = ["permit", "Applicant", "FacilityType", "Address", "status", "FoodItems",
    "Latitude", "Longitude", "dayshours", "Approved", "ExpirationDate"]


if __name__ == '__main__':
    srcpath = argv[1]
    wcsv = DictWriter(stdout, fieldnames=HEADERS)
    wcsv.writeheader()
    with open(srcpath, 'r') as rf:
        rcsv = DictReader(rf)
        for row in rcsv:
            for df in ["Approved", "ExpirationDate"]:
                if row[df]:
                    row[df] = datetime.strptime(row[df], '%m/%d/%Y %I:%M:%S %p').strftime("%Y-%m-%d")

            wcsv.writerow({k: v.strip() for k, v in row.items() if k in HEADERS})
