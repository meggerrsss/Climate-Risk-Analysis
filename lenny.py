import csv
from collections import defaultdict
from pprint import pprint
import requests


SAMPLE_URL = "https://dd.weather.gc.ca/climate/observations/normals/csv/1981-2010/ON/climate_normals_ON_6016527_1981-2010.csv"
def fetch_csv_from_env_can(csv_url):
    with requests.Session() as s:
        download = s.get(csv_url)
        decoded_content = download.content.decode("ISO-8859-1")
        reader = csv.reader(decoded_content.splitlines())
    return list(reader)



def build_chunked_report(csv_rows):
    chunks = defaultdict(list)
    current_chunk = ''
    for row in csv_rows:
        if len(row) == 0:
            continue
        elif len(row) == 1:
            current_chunk = row[0]
        else:
            chunks[current_chunk].append(row)
    return chunks

def dry_days(chunked_report):
    for row in chunked_report["Days with Precipitation"]:
        if row[0] == ">= 0.2 mm":
            return 365 - float(row[-2])
    raise ValueError

with open("example2.csv") as f:
    reader = list(csv.reader(f))

chunked_report = build_chunked_report(reader)

print(dry_days(chunked_report))