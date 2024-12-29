import json
import os
from flask import request
from flask_restful import Resource
from . import flash_card_file_path
from uuid import uuid4


def generate_flash_card_item(title: str, description: str):
    return {
        "_id": uuid4().__str__(),
        "title": title,
        "description": description,
    }


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
        return load_flash_card_list()

    def post(self):
        data = request.get_json()
        flash_card_list = load_flash_card_list()
        new_flash_card = generate_flash_card_item(
            title=data["title"], description=data["description"]
        )
        flash_card_list.append(new_flash_card)
        save_flash_card_list(flash_card_list)
        return new_flash_card


class FlashCardActionWithId(Resource):
    def get(self, id):
        flash_card_list = load_flash_card_list()
        for item in flash_card_list:
            if item["_id"] == id:
                return item
            return None

    def delete(self, id):
        flash_card_list = load_flash_card_list()
        for index, item in flash_card_list:
            if item["_id"] == id:
                flash_card_list.pop(index)
                save_flash_card_list(flash_card_list)
                return {"Note": "Deleted"}
