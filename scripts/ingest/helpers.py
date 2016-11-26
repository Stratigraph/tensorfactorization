import pandas as pd


def extract_base_cameo(cameo_code):
    '''An interface for converting full cameo code to the base-action level (see cameo docs)'''
    if not isinstance(cameo_code, str):
        raise ValueError('CAMEO code was not a string! Good chance of error')

    return cameo_code[:2]


def parse_raw_icews(icews_datatable_fname):
    relcols = ('Event Date', 'Source Country', 'Target Country', 'CAMEO Code')
    renaming = {'Event Date': 'date', 'Source Country': 'source', 'Target Country': 'target', 'CAMEO Code': 'action'}
    icews_df = (pd.read_table(icews_datatable_fname, usecols=relcols, dtype=str, parse_dates=['Event Date'])
                .rename(columns=renaming)
                .assign(action=lambda df: df.action.map(extract_base_cameo)))  # Replace cameo with base code

    return icews_df
