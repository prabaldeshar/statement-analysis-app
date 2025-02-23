from datetime import datetime


def convert_datetime_str_to_datetime(datetime_str: str) -> datetime:
    datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    return datetime_obj
