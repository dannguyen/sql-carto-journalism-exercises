"""
Expects a single filename argument

python scripts/wrangle-congressmembers.py \
   data/raw/congressmembers.csv \
   > data/wrangled/congressmembers.csv
"""

from csv import DictReader, DictWriter
from sys import argv, stdout
HEADERS =  [ "bioguide_id", "title","firstname","middlename", "lastname",
    "name_suffix","nickname", "party","state","district", "senate_class",
    "gender","birthdate", "phone", "fax", "website",
    "congress_office", "fec_id","govtrack_id", "crp_id",
    "twitter_id","youtube_url","facebook_id", "official_rss",]


if __name__ == '__main__':
    srcpath = argv[1]
    with open(srcpath, 'r') as rf:
        rcsv = DictReader(rf)
        wcsv = DictWriter(stdout, fieldnames=HEADERS)
        wcsv.writeheader()
        for row in rcsv:
            if row["in_office"] == '1' and row['title'] in ['Rep', 'Sen']:
                d = {k: v.strip() for k, v in row.items() if k in HEADERS}
                if d['title'] == 'Rep':
                    d['district'] = d['district'].rjust(2, '0')
                wcsv.writerow(d)
