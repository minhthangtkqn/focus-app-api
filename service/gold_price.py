from flask_restful import Resource
from bs4 import BeautifulSoup
import requests
from typing import List, Dict


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


def get_gold_price_from_url():
    url = "https://kimkhanhviethung.vn/tra-cuu-gia-vang.html"
    try:
        html = fetch_html(url)
        gold_prices = parse_gold_price(html)

        for item in gold_prices:
            print(item)
        return gold_prices

    except Exception as e:
        print(f"Error: {e}")


def save_gold_price_to_database():
    pass


class GoldPrice(Resource):
    def get(self):
        return get_gold_price_from_url()
