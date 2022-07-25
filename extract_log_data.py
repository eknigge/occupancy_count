import pandas as pd
import os


def remove_spaces(items: list) -> list:
    out = []
    for i in items:
        out.append(i.strip())
    return out


def format_metadata(data: list) -> dict:
    out = {}
    for i in data:
        element = i.split(":")
        out[element[0]] = element[1]
    return out


def get_dataframe_from_log_files(log_files: list) -> pd.DataFrame:
    datetime_list = []
    data_list = []
    metadata_list = []
    df_list = []

    for file in log_files:
        f = open(file)
        for line in f:
            log_line = line.strip().split('-')
            log_line = remove_spaces(log_line)
            if 'DEBUG' in log_line:
                continue
            elif 'METADATA' in log_line:
                metadata_list.append(log_line[-1])
                continue
            elif len(log_line) < 2:
                continue
            elif len(log_line) >= 7:
                continue
            else:
                datetime_list.append(log_line[0])
                data_list.append(log_line[3])
        metadata = format_metadata(metadata_list)
        df = pd.DataFrame({'DATETIME': pd.to_datetime(datetime_list), 'DATA': data_list})
        for key in metadata:
            df[key] = metadata[key]
        df_list.append(df)
    df_out = pd.concat(df_list)
    return df_out


def main():
    count_files = [i for i in os.listdir(os.getcwd()) if 'count.log' in i]
    df = get_dataframe_from_log_files(count_files)
    df.to_csv('all_data_extracted.csv')


if __name__ == '__main__':
    main()
