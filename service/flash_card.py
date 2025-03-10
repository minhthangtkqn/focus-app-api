import json
import os
from flask import request
from flask_restful import Resource
from service.util import get_database_connection, raw_data_to_list
from . import flash_card_file_path
from uuid import uuid4
from datetime import datetime, timezone


def get_current_time():
    return datetime.now(timezone.utc).isoformat()


def insert_updated_time(flashcard):
    flashcard["_updated"] = get_current_time()
    return flashcard


def generate_flash_card_item(title: str, description: str):
    return {
        "_id": uuid4().__str__(),
        "title": title,
        "description": description,
        "_created": get_current_time(),
        "_updated": None,
    }


def get_flash_card_list_from_db():
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute("select * from cards;")
    rows = db_cursor.fetchall()
    column_name_list = [column_info[0] for column_info in db_cursor.description]
    flash_card_list = raw_data_to_list(rows, column_name_list)
    db_cursor.close()
    db_connection.close()
    return flash_card_list


def get_flash_card_from_db(card_id: str):
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f"select * from cards where _id = '{card_id}';")
    rows = db_cursor.fetchall()
    column_name_list = [column_info[0] for column_info in db_cursor.description]
    flash_card_list = raw_data_to_list(rows, column_name_list)
    db_cursor.close()
    db_connection.close()

    if flash_card_list.__len__() > 0:
        return flash_card_list[0]
    return None


def add_flash_card_to_db(new_data):
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()

    db_cursor.execute(
        f"INSERT INTO cards (_id, title, description, _created, _updated) VALUES (%s, %s, %s, %s, %s);",
        (
            new_data["_id"],
            new_data["title"],
            new_data["description"],
            new_data["_created"],
            f"'{new_data['_updated']}'" if new_data["_updated"] else "NULL",
        ),
    )
    db_connection.commit()

    db_cursor.close()
    db_connection.close()


def update_flash_card_to_db(card_id: str, new_data):
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()

    db_cursor.execute(
        f"update cards set title = '{new_data['title']}', description = '{new_data['description']}', _updated = '{new_data['_updated']}' where _id = '{card_id}';"
    )
    db_connection.commit()

    db_cursor.close()
    db_connection.close()


def delete_flash_card_from_db(card_id: str):
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()

    db_cursor.execute(f"DELETE FROM cards where _id = '{card_id}';")
    db_connection.commit()

    db_cursor.close()
    db_connection.close()


def load_flash_card_list():
    if os.path.exists(flash_card_file_path):
        with open(flash_card_file_path, "r") as f:
            return json.load(f)
    return []


def save_flash_card_list(flash_card_list: list):
    with open(flash_card_file_path, "w") as f:
        json.dump(flash_card_list, f)


class FlashCard(Resource):
    def get(self):
        # return load_flash_card_list()
        return get_flash_card_list_from_db()


class FlashCardActionWithoutId(Resource):
    def post(self, command):
        # if command == "add-card":
        #     data = request.get_json()["data"]
        #     flash_card_list = load_flash_card_list()
        #     new_flash_card = generate_flash_card_item(
        #         title=data["title"], description=data["description"]
        #     )
        #     flash_card_list.append(new_flash_card)
        #     save_flash_card_list(flash_card_list)
        #     return new_flash_card

        # return None

        if command == "add-card":
            submitted_data = request.get_json()["data"]
            new_flash_card = generate_flash_card_item(
                title=submitted_data["title"], description=submitted_data["description"]
            )
            add_flash_card_to_db(new_flash_card)
        return None


class FlashCardActionWithId(Resource):
    def get(self, id):
        # flash_card_list = load_flash_card_list()
        # for item in flash_card_list:
        #     if item["_id"] == id:
        #         return item
        # return None
        return get_flash_card_from_db(id)

    def post(self, id):
        # data = request.get_json()["data"]
        # print("data", data)
        # flash_card_list = load_flash_card_list()
        # for item in flash_card_list:
        #     if item["_id"] == id:
        #         item["title"] = data["title"]
        #         item["description"] = data["description"]
        #         item = insert_updated_time(item)
        #         save_flash_card_list(flash_card_list)
        #         break
        # return {"Note": "Updated"}

        submitted_data = request.get_json()["data"]
        old_data = get_flash_card_from_db(id)
        update_flash_card_to_db(id, insert_updated_time({**old_data, **submitted_data}))
        return {"Note": "Updated"}

    def delete(self, id):
        # flash_card_list = load_flash_card_list()
        # for index, item in enumerate(flash_card_list):
        #     if item["_id"] == id:
        #         flash_card_list.pop(index)
        #         save_flash_card_list(flash_card_list)

        delete_flash_card_from_db(id)
        return {"Note": "Deleted"}


# class DatabaseConnection:
#     def __init__(self, database, user, host, password, port):
#         self.database_connection = psycopg2.connect(
#             database=database,
#             user=user,
#             host=host,
#             password=password,
#             port=port,
#         )

#     def get_database_connection(self):
#         return self.database_connection

#     def get_database_cursor(self):
#         return self.database_connection.cursor()

#     def disconnect_database(self):
#         self.database_connection.close()

#     def save_change_database(self):
#         self.database_connection.commit()


# database_connection = DatabaseConnection(
#     database="postgres",
#     user="postgres",
#     host="localhost",
#     password="12345678",
#     port=5432,
# )

# database_cursor = database_connection.get_database_cursor()
