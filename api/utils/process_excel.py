import pandas as pd
from pandas import DataFrame

file_path = "data/statement-2025-01-01-to-2025-01-01.xlsx"


def find_header_index(df: DataFrame) -> int:
    for index, row in df.iterrows():
        if "ID" in row.values:
            print("ID found in index", index)
            header_index = index
            return header_index

    raise Exception("ID not found in the excel file")


def process_raw_excel(file_path: str) -> DataFrame:
    df = pd.read_excel(file_path, None, dtype=str)

    sheet_name = list(df.keys())[0]
    df = df[sheet_name]

    header_index = find_header_index(df)

    df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=header_index + 1)
    final_df = df.iloc[1:-1, 2:]

    return final_df
