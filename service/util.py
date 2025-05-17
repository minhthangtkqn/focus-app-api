import psycopg2
from const.database import DATABASE_INFO, DATABASE_URL
from datetime import datetime, timezone


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


def get_current_time():
    return datetime.now(timezone.utc).isoformat()


def get_data_list_from_table(table_name: str):
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f"select * from {table_name};")
    rows = db_cursor.fetchall()
    column_name_list = [column_info[0] for column_info in db_cursor.description]
    response_data_list = raw_data_to_list(rows, column_name_list)
    db_cursor.close()
    db_connection.close()
    return response_data_list


def execute_script(script_str: str, script_vars=None):
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute(script_str, script_vars)
    db_connection.commit()
    db_cursor.close()
    db_connection.close()


def create_table(table_name: str, script_str: str):
    execute_script(script_str)
    return f"Create table <{table_name}> successfully!"


def remove_table(table_name: str):
    execute_script(f"""drop table {table_name};""")
    return f"Remove table <{table_name}> successfully!"
