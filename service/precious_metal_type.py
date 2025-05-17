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
            return create_table(
                PRECIOUS_METAL_TYPE__TABLE_NAME,
                f"""create table {PRECIOUS_METAL_TYPE__TABLE_NAME} (
                    {precious_metal_type__table_property['_id']} VARCHAR(255),
                    {precious_metal_type__table_property['name']} VARCHAR(255),
                    {precious_metal_type__table_property['description']} VARCHAR(255),
                    {precious_metal_type__table_property['_created']} VARCHAR(255),
                    {precious_metal_type__table_property['_updated']} VARCHAR(255)
                );""",
            )
        if command == "remove-table":
            return remove_table(PRECIOUS_METAL_TYPE__TABLE_NAME)
        if command == "init-data":
            execute_script(
                f"""insert into {PRECIOUS_METAL_TYPE__TABLE_NAME} (
                    {precious_metal_type__table_property['_id']},
                    {precious_metal_type__table_property['name']},
                    {precious_metal_type__table_property['description']},
                    {precious_metal_type__table_property['_created']},
                    {precious_metal_type__table_property['_updated']}
                ) 
                values 
                    ('14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', 'Vàng Nhẫn Khâu 9999', 'Vàng Nhẫn Khâu 9999', '2025-05-14T15:17:54.423211+00:00', '2025-05-14T15:17:54.423224+00:00')
                ;"""
            )
        return None
