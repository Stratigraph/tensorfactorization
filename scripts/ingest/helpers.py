import pandas as pd


def extract_base_cameo(cameo_code):
    '''An interface for converting full cameo code to the base-action level (see cameo docs)'''
    if not isinstance(cameo_code, str):
        raise ValueError('CAMEO code was not a string! Good chance of error')

    return cameo_code[:2]


def parse_raw_icews(icews_datatable_fname):
    '''Loads an icews table, converts names to shorter version, converts cameo code to base code'''
    relcols = ('Event Date', 'Source Country', 'Target Country', 'CAMEO Code')
    renaming = {'Event Date': 'date', 'Source Country': 'source', 'Target Country': 'target', 'CAMEO Code': 'action'}
    icews_df = (pd.read_table(icews_datatable_fname, usecols=relcols, dtype=str, parse_dates=['Event Date'])
                .rename(columns=renaming)
                .assign(action=lambda df: df.action.map(extract_base_cameo)))  # Replace cameo with base code

    return icews_df


def floor_year_month(dt):
    '''Round a date to the month prior'''
    return pd.to_datetime('{year}-{month}-01'.format(year=dt.year, month=dt.month))


def daily_data_to_monthly(df, month_count_name='count'):
    '''Assumes that has columns date, source, target, action'''
    # Round data down to nearest 
    return (df
            .assign(date=lambda _df: _df.date.map(floor_year_month))  # Round dates down to month
            .groupby(['date', 'source', 'target', 'action']).size()  # Agg by month
            .to_frame(month_count_name)  # Name it as 'count'
            .reset_index())
