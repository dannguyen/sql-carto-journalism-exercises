"""
python scripts/wrangle-schools.py \
   > data/wrangled/schools.csv

"""



from csv import DictReader, DictWriter
from sys import argv, stdout, stderr

DIRECTORY_HEADERS = [
    ("NCESSCH", "nces_id"),
    ("SURVYEAR", "year"),
    ("FIPST", "state_fips"),
    ("STABR", "state"),
    ("LCITY", "city"),
    ("LZIP", "zipcode"),
    ("LEA_NAME", "education_agency"),
    ("SCH_NAME", "name"),
    ("LEVEL", "level"),
    ("OSLO", "low_grade"),
    ("OSHI", "high_grade"),
    ("CHARTER_TEXT", "is_charter"),
]

MEMBERSHIP_HEADERS = [
    ("MEMBER", "enrollment"),
    ("AS", "asian"),
    ("HI", "hispanic"),
    ("BL", "black"),
    ("WH", "white"),
    ("TR", "mixed_race"),
]



LUNCH_HEADERS = [
    ("TOTFRL", "free_or_reduced_lunch_count"),
]

LOCATION_HEADERS = [
    ("CONUM","county_fips"),
    ("CONAME","county"),
    ("CD","congress_district"),
    ("LATCODE","latitude"),
    ("LONGCODE","longitude"),
]


ALL_HEADERS_MAP = dict(DIRECTORY_HEADERS + LOCATION_HEADERS + LUNCH_HEADERS + MEMBERSHIP_HEADERS)

# from docs
# "1 = Primary (low grade = PK through 03; high grade = PK through 08)
# 2 = Middle (low grade = 04 through 07; high grade = 04 through 09)
# 3 = High (low grade = 07 through 12; high grade = 12 only)
# 4 = Other (any other configuration not falling within the above three categories, including ungraded)
# N = Not applicable
LEVEL_MAP = {"1": 'primary', "2": 'middle', "3": 'high', "4": "other", "N": "n/a"}



if __name__ == '__main__':
#    load up all school data files, make them dictionaries
    directory = {s['NCESSCH']: s for s in DictReader(open("./data/raw/school_directory.txt", encoding="latin1").readlines(), delimiter="\t")}
    locations = {s['NCESSCH']: s for s in DictReader(open("./data/raw/school_locations.csv", encoding="latin1").readlines())}
    lunches = {s['NCESSCH']: s for s in DictReader(open("./data/raw/school_lunches.txt", encoding="latin1").readlines(), delimiter="\t")}
    membership = {s['NCESSCH']: s for s in DictReader(open("./data/raw/school_membership.txt", encoding="latin1").readlines(), delimiter="\t")}


    wcsv = DictWriter(stdout, fieldnames=list(ALL_HEADERS_MAP.values()) )
    wcsv.writeheader()





    normal_schools = []
    for n, s_id in enumerate(directory.keys()):
        school = directory[s_id]
        if (school['SCH_TYPE_TEXT'] == 'Regular School' and school['SY_STATUS_TEXT'] in ['Open', 'New']):
            if locations.get(s_id) and lunches.get(s_id) and membership.get(s_id):
                school.update(locations[s_id])
                school.update(lunches[s_id])
                school.update(membership[s_id])
                normal_schools.append(school)


    for school in normal_schools:
        d = {ALL_HEADERS_MAP[k]: v.strip() for k, v in school.items() if k in ALL_HEADERS_MAP.keys()}
        d['level'] = LEVEL_MAP[school['LEVEL']]
        wcsv.writerow(d)
