from flask_restful import Resource
from service.util import (
    create_table,
    execute_script,
    get_data_list_from_table,
    remove_table,
)


PRECIOUS_METAL_TYPE__TABLE_NAME = "precious_metal_type"
precious_metal_type__table_property = {
    "_id": "_id",
    "name": "name",
    "description": "description",
    "_created": "_created",
    "_updated": "_updated",
}


def save_item_to_database(new_data):
    execute_script(
        f"""INSERT INTO {PRECIOUS_METAL_TYPE__TABLE_NAME} (
            {precious_metal_type__table_property['_id']},
            {precious_metal_type__table_property['name']},
            {precious_metal_type__table_property['description']},
            {precious_metal_type__table_property['_created']},
            {precious_metal_type__table_property['_updated']}
        )
        VALUES (%s, %s, %s, %s, %s);""",
        (
            new_data["_id"],
            new_data["name"],
            new_data["description"],
            new_data["_created"],
            f"'{new_data['_updated']}'" if new_data["_updated"] else None,
        ),
    )


class PreciousMetalType(Resource):
    def get(self):
        return get_data_list_from_table(PRECIOUS_METAL_TYPE__TABLE_NAME)


class PreciousMetalTypeActionWithoutId(Resource):
    def post(self, command):
        if command == "create-table":
            # create table
            create_table(
                PRECIOUS_METAL_TYPE__TABLE_NAME,
                f"""create table {PRECIOUS_METAL_TYPE__TABLE_NAME} (
                    {precious_metal_type__table_property['_id']} VARCHAR(255),
                    {precious_metal_type__table_property['name']} VARCHAR(255),
                    {precious_metal_type__table_property['description']} VARCHAR(255),
                    {precious_metal_type__table_property['_created']} VARCHAR(255),
                    {precious_metal_type__table_property['_updated']} VARCHAR(255)
                );""",
            )
            # initialize table data
            execute_script(
                f"""insert into {PRECIOUS_METAL_TYPE__TABLE_NAME} (
                    {precious_metal_type__table_property['_id']},
                    {precious_metal_type__table_property['name']},
                    {precious_metal_type__table_property['description']},
                    {precious_metal_type__table_property['_created']},
                    {precious_metal_type__table_property['_updated']}
                )
                values
                    ('d6e8b2a2-b379-43e8-a9c5-fec7cf88b8ae', 'Vàng Nhẫn Khâu 9999', 'Vàng Nhẫn Khâu 9999', '2025-05-21T15:22:46.089256+00:00', '2025-05-21T15:22:46.089287+00:00'),
                    ('973d6e9b-4cef-4341-8ff4-62728b71593c', 'Vàng Nhẫn Khâu 98', 'Vàng Nhẫn Khâu 98', '2025-05-21T15:22:48.769124+00:00', '2025-05-21T15:22:48.769146+00:00'),
                    ('553489a9-1321-447a-9ce7-38b0a7fc95e5', 'Vàng Nhẫn Khâu 97 ( Quảng Nam )', 'Vàng Nhẫn Khâu 97 ( Quảng Nam )', '2025-05-21T15:22:50.483551+00:00', '2025-05-21T15:22:50.483614+00:00'),
                    ('9dd7f790-cc2b-49db-a595-a3adb10f0c78', 'Vàng Nhẫn Khâu 96', 'Vàng Nhẫn Khâu 96', '2025-05-21T15:22:52.129157+00:00', '2025-05-21T15:22:52.129181+00:00'),
                    ('28aa2ac0-920f-40a9-a120-c228055928e5', 'Nữ trang 980', 'Nữ trang 980', '2025-05-21T15:22:53.754727+00:00', '2025-05-21T15:22:53.754781+00:00'),
                    ('a231d397-4ffe-4bbc-9bd0-bf0527773f1a', 'Vàng công ty 610', 'Vàng công ty 610', '2025-05-21T15:22:55.383035+00:00', '2025-05-21T15:22:55.383081+00:00'),
                    ('f0be90bb-0522-4528-99d4-fee55732f476', 'Vàng đúc', 'Vàng đúc', '2025-05-21T15:22:57.934556+00:00', '2025-05-21T15:22:57.934713+00:00'),
                    ('0fd17025-f93f-494b-a4ae-73db4c35bc9e', 'Bạc trang sức', 'Bạc trang sức', '2025-05-21T15:23:00.552601+00:00', '2025-05-21T15:23:00.552669+00:00'),
                    ('335ddaf9-c6c9-4778-b172-fa90b5392339', 'Vàng 417', 'Vàng 417', '2025-05-25T13:37:40.713293+00:00', '2025-05-25T13:37:40.713307+00:00')
                ;"""
            )
        if command == "remove-table":
            return remove_table(PRECIOUS_METAL_TYPE__TABLE_NAME)
        return None
