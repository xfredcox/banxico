import datetime as dt
import json
import logging
import requests
import sys
import os.path


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG) # TODO: Remove
log = logging.getLogger(__name__)

DESTINATION_DIR = './db'
MAX_SERIES_LOOKUP = 20

# Token limit for historical lookups: 100 per 5 minutes, 5000 per day
# The chunked lookup below requires just 2 queries so no need for token rotation...
TOKEN = "885cbd0a7c94b1c24efac9444f1ec75bb5241321daa1e28837d2dd235b81d623"
URL = "https://www.banxico.org.mx/SieAPIRest/service/v1/series/{series}/datos?token={token}"

SERIES = (
    ("CETES", "Banco de Mexico", "SF9734"),
    ("CETES", "Development Banks", "SF117781"),
    ("CETES", "Commercial Banks", "SF117782"),
    ("CETES", "Public Sector", "SF117722"),
    ("CETES", "Siefores", "SF118542"),
    ("CETES", "Domestic Private Sector", "SF112910"),
    ("CETES", "Foreign Private Sector", "SF320748"),

    ("BONDES", "Banco de Mexico", "SF9738"),
    ("BONDES", "Development Banks", "SF117783"),
    ("BONDES", "Commercial Banks", "SF117784"),
    ("BONDES", "Public Sector", "SF117723"),
    ("BONDES", "Siefores", "SF118543"),
    ("BONDES", "Domestic Private Sector", "SF112911"),
    ("BONDES", "Foreign Private Sector", "SF320749"),

    ("BONDES D", "Banco de Mexico", "SF60435"),
    ("BONDES D", "Development Banks", "SF112906"),
    ("BONDES D", "Commercial Banks", "SF112907"),
    ("BONDES D", "Public Sector", "SF117724"),
    ("BONDES D", "Siefores", "SF118544"),
    ("BONDES D", "Domestic Private Sector", "SF112912"),
    ("BONDES D", "Foreign Private Sector", "SF320750"),

    ("UDIBONOS", "Banco de Mexico", "SF9739"),
    ("UDIBONOS", "Development Banks", "SF117785"),
    ("UDIBONOS", "Commercial Banks", "SF117786"),
    ("UDIBONOS", "Public Sector", "SF117725"),
    ("UDIBONOS", "Siefores", "SF118545"),
    ("UDIBONOS", "Domestic Private Sector", "SF112913"),
    ("UDIBONOS", "Foreign Private Sector", "SF320751"),

    ("BONOS", "Banco de Mexico", "SF18569"),
    ("BONOS", "Development Banks", "SF112908"),
    ("BONOS", "Commercial Banks", "SF112909"),
    ("BONOS", "Public Sector", "SF117726"),
    ("BONOS", "Siefores", "SF118546"),
    ("BONOS", "Domestic Private Sector", "SF112914"),
    ("BONOS", "Foreign Private Sector", "SF320752"),
)

SERIES = dict((x[2], (x[0], x[1])) for x in SERIES)


def chunk(_iter, chunk_size):
    for i in range(0, len(_iter), chunk_size):
        yield _iter[i:i+chunk_size]


def parse_records(json_resp):
    data = json_resp['bmx']['series']
    records = []
    
    for series_record in data:
        series_id = series_record['idSerie']
        series_title = series_record['titulo']
        instrument_type, short_name = SERIES[series_id]
        log.debug("Casting values for %s %s", instrument_type, short_name)
            
        for entry in series_record['datos']:
            records.append({
                'value': float(entry['dato'].replace(',', '')),
                'date': dt.datetime.strptime(entry['fecha'], "%d/%m/%Y").isoformat(),
                'series_id': series_id,
                'original_title': series_title,
                'instrument_type': instrument_type,
                'short_name': short_name,
            })

    return records

        
def main():
    run_timestamp = dt.datetime.now().isoformat()
    log.info("Running Banxico Crawl for %s", run_timestamp)

    records = []

    # Series are chunked to comply with REST API MAX_SERIES_LOOKUP per query.
    for query_series_chunk in chunk(list(SERIES.keys()), MAX_SERIES_LOOKUP):
        log.info("Requesting data for %s", query_series_chunk)
        resp = requests.get(URL.format(series=','.join(query_series_chunk), token=TOKEN))        
        records.extend(parse_records(resp.json()))

    log.debug("Converting to JSON string")        
    output = json.dumps(records)

    filename = "db.%s.json" % run_timestamp
    filepath = os.path.join(DESTINATION_DIR, filename)
    log.info("Saving to file: %s", filepath)
    
    with open(filepath, 'w') as f:
        f.write(output)

    # Updating db.json to reflect the latest data.
    # TODO: implement this as a symlink. Keeping it as a separate copy for now on the off
    # chance this gets run on Windows.
    filepath = os.path.join(DESTINATION_DIR, "db.json")
    log.info("Saving to file: %s", filepath)
    with open(filepath, 'w') as f:
        f.write(output)
        
    log.info("Crawl Completed")    


if __name__ == "__main__":
    main()
