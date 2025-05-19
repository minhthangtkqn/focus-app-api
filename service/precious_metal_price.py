from flask_restful import Resource
from bs4 import BeautifulSoup
import requests
from typing import List, Dict
from service.precious_metal_type import (
    PRECIOUS_METAL_TYPE__TABLE_NAME,
    save_item_to_database as save_type_to_database,
    precious_metal_type__table_property,
)
from service.util import (
    create_table,
    execute_script,
    get_current_time,
    get_data_list_from_table,
    get_data_list_from_table_by_script,
    remove_table,
)
from price_parser import Price
from uuid import uuid4

PRECIOUS_METAL_PRICE__URL = "https://kimkhanhviethung.vn/tra-cuu-gia-vang.html"
PRECIOUS_METAL_PRICE__TABLE_NAME = "precious_metal_price"
precious_metal_price_table_property = {
    "_id": "_id",
    "type_id": "type_id",
    "buy_price": "buy_price",
    "sell_price": "sell_price",
    "_created": "_created",
    "_updated": "_updated",
}


# START - HTML PARSING
def fetch_html(url: str) -> str:
    """Fetch raw HTML from the target URL."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; GoldScraper/1.0)"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise error if request fails
    return response.text


def parse_precious_metal_price(html_str: str) -> List[Dict[str, str]]:
    """Parse the precious metal price table and return data."""
    soup = BeautifulSoup(html_str, "html.parser")

    table = soup.find(class_="table_goldprice")
    rows = table.find_all("tr")
    response_data = []
    spec_sell_price = None
    precious_metal_type_list = get_data_list_from_table(PRECIOUS_METAL_TYPE__TABLE_NAME)

    for row in rows[1:]:
        cols = row.find_all("td")
        if not cols:
            continue
        spec_buy_price = Price.fromstring(cols[1].get_text(strip=True))
        spec_sell_price = Price.fromstring(cols[2].get_text(strip=True))
        if spec_buy_price is not None:
            spec_buy_price = int(spec_buy_price.amount)
        if spec_sell_price is not None:
            spec_sell_price = int(spec_sell_price.amount)

        # check if type of row existed
        current_precious_metal_name = cols[0].get_text(strip=True)
        current_precious_metal_type = next(
            (
                type
                for type in precious_metal_type_list
                if type["name"] == current_precious_metal_name
            ),
            None,
        )
        if current_precious_metal_type:
            will_saved_type_id = current_precious_metal_type["_id"]
        else:
            will_saved_type_id = uuid4().__str__()
            save_type_to_database(
                new_data={
                    precious_metal_type__table_property["_id"]: will_saved_type_id,
                    precious_metal_type__table_property[
                        "name"
                    ]: current_precious_metal_name,
                    precious_metal_type__table_property[
                        "description"
                    ]: current_precious_metal_name,
                    precious_metal_type__table_property["_created"]: get_current_time(),
                    precious_metal_type__table_property["_updated"]: get_current_time(),
                }
            )

        new_item = {
            precious_metal_price_table_property["_id"]: uuid4().__str__(),
            precious_metal_price_table_property["type_id"]: will_saved_type_id,
            precious_metal_price_table_property["buy_price"]: spec_buy_price,
            precious_metal_price_table_property["sell_price"]: spec_sell_price,
            precious_metal_price_table_property["_created"]: get_current_time(),
            precious_metal_price_table_property["_updated"]: get_current_time(),
        }
        save_item_to_database(new_item)
        response_data.append(
            {
                **new_item,
                "type_name": current_precious_metal_name,
            }
        )

    return response_data


# END - HTML PARSING


def get_gold_price_from_url():
    try:
        html = fetch_html(PRECIOUS_METAL_PRICE__URL)
        return parse_precious_metal_price(html)

    except Exception as e:
        print(f"Error: {e}")


def save_item_to_database(new_data):
    execute_script(
        f"""INSERT INTO {PRECIOUS_METAL_PRICE__TABLE_NAME} (
            {precious_metal_price_table_property['_id']},
            {precious_metal_price_table_property['type_id']},
            {precious_metal_price_table_property['buy_price']},
            {precious_metal_price_table_property['sell_price']},
            {precious_metal_price_table_property['_created']},
            {precious_metal_price_table_property['_updated']}
        )
        VALUES (%s, %s, %s, %s, %s, %s);""",
        (
            new_data["_id"],
            new_data["type_id"],
            new_data["buy_price"],
            new_data["sell_price"],
            new_data["_created"],
            f"'{new_data['_updated']}'" if new_data["_updated"] else None,
        ),
    )


class PreciousMetalPrice(Resource):
    def get(self):
        return get_gold_price_from_url()


class PreciousMetalPriceList(Resource):
    def get(self):
        return get_data_list_from_table_by_script(
            f"""select 
                {PRECIOUS_METAL_PRICE__TABLE_NAME}.{precious_metal_price_table_property['_id']},
                {PRECIOUS_METAL_PRICE__TABLE_NAME}.{precious_metal_price_table_property['type_id']},
                {PRECIOUS_METAL_TYPE__TABLE_NAME}.{precious_metal_type__table_property['name']} as type_name,
                {PRECIOUS_METAL_PRICE__TABLE_NAME}.{precious_metal_price_table_property['buy_price']},
                {PRECIOUS_METAL_PRICE__TABLE_NAME}.{precious_metal_price_table_property['sell_price']},
                {PRECIOUS_METAL_PRICE__TABLE_NAME}.{precious_metal_price_table_property['_created']},
                {PRECIOUS_METAL_PRICE__TABLE_NAME}.{precious_metal_price_table_property['_updated']}
            from {PRECIOUS_METAL_TYPE__TABLE_NAME} join {PRECIOUS_METAL_PRICE__TABLE_NAME}
            on {PRECIOUS_METAL_TYPE__TABLE_NAME}.{precious_metal_type__table_property['_id']} = {PRECIOUS_METAL_PRICE__TABLE_NAME}.{precious_metal_price_table_property['type_id']}
            order by {PRECIOUS_METAL_PRICE__TABLE_NAME}.{precious_metal_price_table_property['_created']} asc;
            ;"""
        )


class PreciousMetalPriceActionWithoutId(Resource):
    def post(self, command):
        if command == "create-table":
            # create table
            create_table(
                PRECIOUS_METAL_PRICE__TABLE_NAME,
                f"""create table {PRECIOUS_METAL_PRICE__TABLE_NAME} (
                    {precious_metal_price_table_property['_id']} VARCHAR(255),
                    {precious_metal_price_table_property['type_id']} VARCHAR(255),
                    {precious_metal_price_table_property['buy_price']} INTEGER,
                    {precious_metal_price_table_property['sell_price']} INTEGER,
                    {precious_metal_price_table_property['_created']} VARCHAR(255),
                    {precious_metal_price_table_property['_updated']} VARCHAR(255)
                );""",
            )
            # initialize table data
            execute_script(
                f"""insert into {PRECIOUS_METAL_PRICE__TABLE_NAME} (
                    {precious_metal_price_table_property['_id']},
                    {precious_metal_price_table_property['type_id']},
                    {precious_metal_price_table_property['buy_price']},
                    {precious_metal_price_table_property['sell_price']},
                    {precious_metal_price_table_property['_created']},
                    {precious_metal_price_table_property['_updated']}
                ) 
                values 
                    ('635d2be4-6f1a-4f75-98ea-3956f0232005', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10780000, '2025-05-14T15:17:54.423211+00:00', '2025-05-14T15:17:54.423224+00:00'),
                    ('09cc37ce-ceda-426d-ad7c-e596c57355c0', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10780000, '2025-05-14T15:51:16.968321+00:00', '2025-05-14T15:51:16.968332+00:00'),
                    ('ffb6b78c-5685-4d71-9596-7646d74acd60', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10780000, '2025-05-14T15:51:22.368627+00:00', '2025-05-14T15:51:22.368637+00:00'),
                    ('000c6d5f-6976-46fd-a966-132ab0e9325d', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10780000, '2025-05-14T15:51:23.583920+00:00', '2025-05-14T15:51:23.583931+00:00'),
                    ('5b2bf729-2344-4a56-a25f-21c65c2c1ab2', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10780000, '2025-05-14T15:51:32.257781+00:00', '2025-05-14T15:51:32.257790+00:00'),
                    ('241faeb1-3a04-4d96-a5b9-5caa5060b1e5', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10780000, '2025-05-14T16:01:52.544847+00:00', '2025-05-14T16:01:52.544857+00:00'),
                    ('a6b60ab9-e004-4b44-af13-5743ecb35ba2', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10780000, '2025-05-14T16:01:54.322079+00:00', '2025-05-14T16:01:54.322098+00:00'),
                    ('8e2aa21d-d57d-47e4-a349-471d3af15885', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10780000, '2025-05-14T16:33:08.286238+00:00', '2025-05-14T16:33:08.286249+00:00'),
                    ('1dd0d30b-ac4d-4c5b-874d-beee2b825a6b', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10780000, '2025-05-14T16:35:11.251227+00:00', '2025-05-14T16:35:11.251238+00:00'),
                    ('b84e0465-6331-4913-88d0-56f3bc7277b2', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10780000, '2025-05-14T16:43:44.089716+00:00', '2025-05-14T16:43:44.089725+00:00'),
                    ('543a147c-2855-4bcd-9376-9b0b2e50349c', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10780000, '2025-05-14T16:50:15.182781+00:00', '2025-05-14T16:50:15.182796+00:00'),
                    ('0eb93f98-ba07-4bfe-9a8a-eb45432f10f9', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10780000, '2025-05-14T16:51:52.252469+00:00', '2025-05-14T16:51:52.252480+00:00'),
                    ('3099acd1-3119-449d-9cdf-1399e307e05b', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10780000, '2025-05-14T16:51:56.621429+00:00', '2025-05-14T16:51:56.621438+00:00'),
                    ('161761a8-bf86-4c1c-bb62-24d2702bdcd7', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10780000, '2025-05-14T16:51:58.848849+00:00', '2025-05-14T16:51:58.848860+00:00'),
                    ('bdc599f0-08eb-440e-8960-3f1cd0f73f39', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10780000, '2025-05-14T16:59:16.034303+00:00', '2025-05-14T16:59:16.034314+00:00'),
                    ('5b0e808f-b6d3-468d-a9f0-4278719c03eb', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10710000, '2025-05-15T02:49:24.202564+00:00', '2025-05-15T02:49:24.202600+00:00'),
                    ('885393ca-2613-415a-a291-9a1871afd1a6', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10660000, '2025-05-15T04:17:46.406496+00:00', '2025-05-15T04:17:46.406527+00:00'),
                    ('5507d365-f437-48eb-a143-e4ac64f20638', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10660000, '2025-05-15T04:18:22.210913+00:00', '2025-05-15T04:18:22.210927+00:00'),
                    ('bb9ca284-21be-454d-9d6e-da4a158321a4', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10660000, '2025-05-15T04:20:57.608197+00:00', '2025-05-15T04:20:57.608210+00:00'),
                    ('08774b62-b33d-426b-a19d-0c9b009b7f88', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10660000, '2025-05-15T04:27:16.403513+00:00', '2025-05-15T04:27:16.403529+00:00'),
                    ('eba69998-3078-483c-a171-d415f022c7e4', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10610000, '2025-05-15T07:30:46.292357+00:00', '2025-05-15T07:30:46.292384+00:00'),
                    ('eec18d96-4245-4a1a-bb94-03aa42feff60', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10610000, '2025-05-15T07:30:46.890990+00:00', '2025-05-15T07:30:46.891012+00:00'),
                    ('bbe0913d-70cc-449d-85cb-80cd6fce1505', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10610000, '2025-05-15T07:31:04.193758+00:00', '2025-05-15T07:31:04.193773+00:00'),
                    ('f6b416c9-2671-4ae2-9f61-815bec5761d1', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10630000, '2025-05-15T09:41:01.623594+00:00', '2025-05-15T09:41:01.623611+00:00'),
                    ('1f72b2c1-a158-441c-a380-f7db538e6551', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10840000, '2025-05-16T02:17:17.757029+00:00', '2025-05-16T02:17:17.757048+00:00'),
                    ('3095521f-e726-4ff6-af01-1050a8411282', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10840000, '2025-05-16T02:39:07.550869+00:00', '2025-05-16T02:39:07.550890+00:00'),
                    ('1067f12e-96ab-4e18-9b89-d7e09c306c7f', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10840000, '2025-05-16T02:40:11.663188+00:00', '2025-05-16T02:40:11.663208+00:00'),
                    ('1d82db9f-ebcf-483d-9188-51b53eafe62a', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10780000, '2025-05-16T04:02:05.791423+00:00', '2025-05-16T04:02:05.791440+00:00'),
                    ('c17a2e91-ad73-4b69-b252-3aa2cbcb4c52', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10780000, '2025-05-16T04:18:48.483388+00:00', '2025-05-16T04:18:48.483411+00:00'),
                    ('58621814-6d41-490f-9329-b4ca716188f8', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10750000, '2025-05-16T08:32:52.872374+00:00', '2025-05-16T08:32:52.872389+00:00'),
                    ('97366cab-7ee0-46d5-99e9-ef1575e88e7b', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10750000, '2025-05-16T08:56:13.367555+00:00', '2025-05-16T08:56:13.367585+00:00'),
                    ('b4075c50-8010-4044-b513-7b07fc6936d0', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10650000, '2025-05-16T15:22:08.313875+00:00', '2025-05-16T15:22:08.313887+00:00'),
                    ('8c5e1ef6-3c5b-468c-8030-1c79b44a7f98', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10670000, '2025-05-17T01:56:18.150979+00:00', '2025-05-17T01:56:18.150999+00:00'),
                    ('d585d0c9-8f09-4dd6-8390-d60d0cc16ed0', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10670000, '2025-05-17T02:45:58.389163+00:00', '2025-05-17T02:45:58.389180+00:00'),
                    ('95642042-b7e9-4587-b8eb-a03cfc1bca07', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10670000, '2025-05-17T04:34:45.273802+00:00', '2025-05-17T04:34:45.273832+00:00'),
                    ('1d667e12-b05a-482a-acd1-fd09b51f2468', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10670000, '2025-05-17T04:47:39.776686+00:00', '2025-05-17T04:47:39.776701+00:00'),
                    ('8c93a06b-0eb8-48cc-882d-ccb3cad8fba1', '14f3b6dd-6135-4b4e-a85a-a53e2ce2362e', null, 10670000, '2025-05-17T11:27:49.470877+00:00', '2025-05-17T11:27:49.470892+00:00')
                ;"""
            )
        if command == "remove-table":
            return remove_table(PRECIOUS_METAL_PRICE__TABLE_NAME)
        return None
