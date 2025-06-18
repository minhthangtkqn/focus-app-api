from flask_restful import Resource
from bs4 import BeautifulSoup
import requests
from typing import List, Dict
from service.util import (
    create_table,
    get_current_time,
    get_data_list_from_table,
    get_database_connection,
    remove_table,
)
from price_parser import Price
from uuid import uuid4
import warnings

GOLD_PRICE_URL = "https://kimkhanhviethung.vn/tra-cuu-gia-vang.html"
GOLD_PRICE_TABLE_NAME = "gold_price"
gold_price_table_property = {
    "_id": "_id",
    "price": "price",
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


def parse_gold_price(html_str: str) -> List[Dict[str, str]]:
    """Parse the gold price table and return data."""
    soup = BeautifulSoup(html_str, "html.parser")

    table = soup.find(class_="table_goldprice")
    rows = table.find_all("tr")
    data = None
    spec_sell_gold_price = None

    for row in rows[1:]:
        cols = row.find_all("td")
        if not cols:
            continue
        if cols[0].get_text(strip=True) == "Vàng Nhẫn Khâu 9999":
            spec_sell_gold_price = Price.fromstring(cols[2].get_text(strip=True))
            if spec_sell_gold_price is not None:
                spec_sell_gold_price = int(spec_sell_gold_price.amount)
        # val = {
        #     "name": cols[0].get_text(strip=True),
        #     "buy_price": cols[1].get_text(strip=True),
        #     "sell_price": cols[2].get_text(strip=True),
        # }
        # data.append(val)
        data = spec_sell_gold_price

    save_item_to_database(
        new_data={
            gold_price_table_property["_id"]: uuid4().__str__(),
            gold_price_table_property["price"]: spec_sell_gold_price,
            gold_price_table_property["_created"]: get_current_time(),
            gold_price_table_property["_updated"]: get_current_time(),
        }
    )

    return data


# END - HTML PARSING


def get_gold_price_from_url():
    try:
        html = fetch_html(GOLD_PRICE_URL)
        gold_prices = parse_gold_price(html)

        # for item in gold_prices:
        #     print(item)
        return gold_prices

    except Exception as e:
        print(f"Error: {e}")


def save_item_to_database(new_data):
    print("new_data", new_data)
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute(
        f"""INSERT INTO {GOLD_PRICE_TABLE_NAME} (
            {gold_price_table_property['_id']},
            {gold_price_table_property['price']},
            {gold_price_table_property['_created']},
            {gold_price_table_property['_updated']}
        )
        VALUES (%s, %s, %s, %s);""",
        (
            new_data["_id"],
            new_data["price"],
            new_data["_created"],
            f"'{new_data['_updated']}'" if new_data["_updated"] else None,
        ),
    )
    db_connection.commit()
    db_cursor.close()
    db_connection.close()


class GoldPrice(Resource):
    warnings.warn("This class is deprecated. Use PreciousMetalPrice instead.")

    def get(self):
        return get_gold_price_from_url()


class GoldPriceList(Resource):
    warnings.warn("This class is deprecated. Use PreciousMetalPrice instead.")

    def get(self):
        return get_data_list_from_table(GOLD_PRICE_TABLE_NAME)


class GoldPriceActionWithoutId(Resource):
    warnings.warn("This class is deprecated. Use PreciousMetalPrice instead.")

    def post(self, command):
        if command == "create-table":
            return create_table(
                table_name=GOLD_PRICE_TABLE_NAME,
                create_table_script=f"""create table {GOLD_PRICE_TABLE_NAME} (
                    {gold_price_table_property['_id']} VARCHAR(255),
                    {gold_price_table_property['price']} INTEGER,
                    {gold_price_table_property['_created']} VARCHAR(255),
                    {gold_price_table_property['_updated']} VARCHAR(255)
                );""",
            )
        if command == "remove-table":
            return remove_table(GOLD_PRICE_TABLE_NAME)
        return None
