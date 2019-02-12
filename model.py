from functools import lru_cache
import json
import pandas as pd

from crawler import get_latest_path


# TODO: implement some cache busting to reflect updates to the underlying data.
@lru_cache(1)
def get_latest_data():
    path = get_latest_path()
    
    with open(path, 'r') as f:
        data = json.loads(f.read())
        df = pd.DataFrame(data)
        return df


@lru_cache(1)
def get_total_by_instrument():
    df = get_latest_data()
    df = df.groupby(['date', 'instrument_type'])['value'].sum()
    return df.unstack()


@lru_cache(128)
def get_total_by_sector(instrument_types=None):
    df = get_latest_data()
    if instrument_types is not None:
        df = df[df['instrument_type'].isin(instrument_types)]
    df = df.groupby(['date', 'short_name'])['value'].sum()
    return df.unstack()
