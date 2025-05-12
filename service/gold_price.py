from flask_restful import Resource
from bs4 import BeautifulSoup
import requests
from typing import List, Dict

from service.util import get_database_connection

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

    # table = soup.select("div.table_goldprice table")
    table = soup.find(class_="table_goldprice")
    rows = table.find_all("tr")
    data = []
    headers = [th.get_text(strip=True) for th in rows[0].find_all("th")]

    for row in rows[1:]:
        cols = row.find_all("td")
        if not cols:
            continue
        values = [td.get_text(strip=True) for td in cols]
        entry = dict(zip(headers, values))
        data.append(entry)

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


def create_gold_price_table():
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute(
        f"""create table {GOLD_PRICE_TABLE_NAME} (
            {gold_price_table_property['_id']} VARCHAR(255),
            {gold_price_table_property['price']} INTEGER,
            {gold_price_table_property['_created']} VARCHAR(255),
            {gold_price_table_property['_updated']} VARCHAR(255)
        );"""
    )
    db_connection.commit()
    db_cursor.close()
    db_connection.close()
    return "Create table successfully!"


def remove_gold_price_table():
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()
    db_cursor.execute(f"""drop table {GOLD_PRICE_TABLE_NAME};""")
    db_connection.commit()
    db_cursor.close()
    db_connection.close()
    return "Remove table successfully!"


def save_gold_price_to_database(new_data):
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()

    db_cursor.execute(
        f"""INSERT INTO {GOLD_PRICE_TABLE_NAME} (
            {gold_price_table_property['_id']}.
            {gold_price_table_property['price']}.
            {gold_price_table_property['_created']}.
            {gold_price_table_property['_updated']}
        )
        VALUES (
            {new_data["_id"]},
            {new_data["price"]},
            {new_data["_created"]},
            {f"'{new_data['_updated']}'" if new_data["_updated"] else None}
        );"""
    )

    db_connection.commit()
    db_cursor.close()
    db_connection.close()


class GoldPrice(Resource):
    def get(self):
        return get_gold_price_from_url()


class GoldPriceActionWithoutId(Resource):
    def post(self, command):
        if command == "create-table":
            return create_gold_price_table()
        if command == "remove-table":
            return remove_gold_price_table()
        return None
