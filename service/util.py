import psycopg2
from const.database import DATABASE_INFO, DATABASE_URL


def get_database_connection():
    # return psycopg2.connect(**DATABASE_INFO) # shorter code, but not good IDE typing (for now)

    # Use this when using OFFLINE database
    # return psycopg2.connect(
    #     database=DATABASE_INFO["database"],
    #     user=DATABASE_INFO["user"],
    #     host=DATABASE_INFO["host"],
    #     password=DATABASE_INFO["password"],
    #     port=DATABASE_INFO["port"],
    # )

    # Use this when using ONLINE database
    return psycopg2.connect(DATABASE_URL)


def raw_data_to_list(raw_row_list_data: list[tuple], column_name_list: list):
    normalize_list = []
    for row in raw_row_list_data:
        returned_row = {}
        for column_name_index, column_name in enumerate(column_name_list):
            returned_row[column_name] = row[column_name_index]
        normalize_list.append(returned_row)
    return normalize_list
