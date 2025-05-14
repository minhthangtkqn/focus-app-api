import json
import os
from flask import request
from flask_restful import Resource
from service.util import get_current_time, get_database_connection, raw_data_to_list
from . import flash_card_file_path
from uuid import uuid4


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


def create_flash_card_db():
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute(
        """create table cards (
        _id VARCHAR(255),
        title VARCHAR(255),
        description VARCHAR(255),
        _created VARCHAR(255),
        _updated VARCHAR(255)
    );"""
    )
    db_connection.commit()
    db_cursor.close()
    db_connection.close()


def init_flash_card_db():
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute(
        """insert into cards (_id, title, description, _created, _updated) 
        values 
            ('420e72a4-7a71-4045-b29d-a5a3f8aff4bf', 'Table', 'a device with four legs and a flat surface.', '2025-01-12T07:50:32.019992+00:00', null),
            ('6984c72a-6e24-4d6c-b4d5-a7e00add74ff', 'Chair', 'a seat for one person that has a back, usually four legs, and sometimes two arms.', '2025-01-12T07:50:32.019992+00:00', null),
            ('13997e6d-0d5f-4841-8451-8f59886740da', 'Comb', 'a flat piece of plastic, wood, or metal with a thin row of long, narrow parts along one side, used to tidy and arrange your hair.', '2025-01-12T07:50:32.019992+00:00', null),
            ('4010f0a9-0112-4c89-9b81-9698624cc7ae', 'Paper', 'thin, flat material made from crushed wood or cloth, used for writing, printing, or drawing on.', '2025-01-12T07:50:32.019992+00:00', null),
            ('4010f0a9-0112-4c89-9b81-9698624cc7ab', 'Smartphone', 'A pocket-sized computer that combines a mobile phone with internet access, a camera, and various apps.', '2025-01-12T07:50:32.019992+00:00', null),
            ('4010f0a9-0112-4c89-9b81-9698624cc7ac', 'Bottle', 'A container, usually made of glass or plastic, with a narrow neck for holding liquids.', '2025-01-12T07:50:32.019992+00:00', null),
            ('4010f0a9-0112-4c89-9b81-9698624cc7aa', 'Monitor', 'A display device that visually presents information from a computer.', '2025-01-12T07:50:32.019992+00:00', null),
            ('dbc4910d-229b-49d2-8ac6-bf76ea468a50', 'month', 'a period of about four weeks, especially one of the twelve periods into which a year is divided.', '2025-01-12T07:50:32.019992+00:00', null),
            ('550ca6b1-0cad-4a11-aa02-b4d21f73e3c2', 'Piano', 'A keyboard musical instrument with 88 keys, producing sounds through hammers striking strings.', '2025-01-12T07:50:32.019992+00:00', null),
            ('5d8888ad-f62e-424c-95e3-894d6fca3ed1', 'Coat', 'An outer garment worn for warmth and protection from the elements.', '2025-01-12T07:50:32.019992+00:00', null),
            ('4b76d2c0-e44d-48f8-99b1-79d649ba1263', 'Shirt', 'A garment worn on the upper body, typically with sleeves.', '2025-01-12T07:50:32.019992+00:00', null),
            ('a90c6adb-1832-4249-b6f0-d1911b9f0e94', 'Ruler', 'A flat, straight tool used for measuring length or drawing straight lines.', '2025-01-12T07:50:32.019992+00:00', null),
            ('37f90f13-06c3-47ab-b27d-389892ab93d2', 'Pen', 'A writing instrument that uses ink to create marks on paper.', '2025-01-12T07:50:32.019992+00:00', null),
            ('ddbe2885-cc6d-4058-9345-16a58da086fc', 'Window', 'An opening in a wall or vehicle that allows light and air to pass through.', '2025-01-12T07:50:32.019992+00:00', null),
            ('9c9a84eb-5db0-45dd-aa60-0663d295fa21', 'Cup', 'A small, open container used for drinking, typically made of ceramic, glass, or plastic.', '2025-01-12T07:50:32.019992+00:00', null),
            ('90650070-c2a8-4fdb-8338-480b2ff163b7', 'CPU', 'Brain of the computer, performs calculations.', '2025-01-12T07:50:32.019992+00:00', null)
            ('3a390960-f78a-40fc-893c-273c613c2669', 'Box', 'A container with flat sides, often rectangular, used for storing or transporting items.', '2025-01-12T07:50:32.019992+00:00', null)
            ('7f3dcbab-66e0-4e61-831f-9a8c96101ea9', 'Keyboard', 'A panel of keys that allows a user to input text and commands into a computer or other electronic device.', '2025-01-12T07:50:32.019992+00:00', null)
            ('5a11cd55-b6eb-4452-9252-279c7724ac1d', 'Pillow', 'A soft cushion used to support the head or body, typically while sleeping or resting.', '2025-01-12T07:50:32.019992+00:00', null)
        ;"""
    )
    db_connection.commit()
    db_cursor.close()
    db_connection.close()


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
            f"'{new_data['_updated']}'" if new_data["_updated"] else None,
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

        if command == "create-table":
            create_flash_card_db()

        if command == "init-data":
            init_flash_card_db()

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
