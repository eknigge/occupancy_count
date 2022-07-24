import pandas as pd
import datetime
import numpy as np
import json


def is_am_or_pm(value: datetime) -> str:
    noon = datetime.time(hour=12)
    value = pd.to_datetime(value).time()
    if value < noon:
        return 'AM'
    else:
        return 'PM'


def add_date_data(df: pd.DataFrame) -> pd.DataFrame:
    df['DATE'] = pd.to_datetime(df['DATETIME']).dt.date
    df['TIME_PERIOD'] = df['DATETIME'].apply(is_am_or_pm)
    return df


def get_summary_table(df: pd.DataFrame) -> pd.DataFrame:
    table = df.pivot_table(values='DATETIME',
                           index=['DATE', 'TIME_PERIOD', 'Direction', 'Lane', 'Location'],
                           columns='DATA', aggfunc=np.count_nonzero)
    return table


def get_time_period_summary(df: pd.DataFrame) -> pd.DataFrame:
    table = df.pivot_table(values='DATETIME', index='TIME_PERIOD',
                           columns='DATA', aggfunc=np.count_nonzero)
    return table


def main():
    all_data_filename = 'all_data_extracted.csv'
    df = pd.read_csv(all_data_filename)
    df = add_date_data(df)

    # get summary tables
    summary_table = get_summary_table(df)
    time_period_table = get_time_period_summary(df)

    with pd.ExcelWriter('summary_results.xlsx') as writer:
        summary_table.to_excel(writer, sheet_name='summary_results')
        time_period_table.to_excel(writer, sheet_name='time_period_results')


if __name__ == '__main__':
    main()
