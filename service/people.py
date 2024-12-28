import os
import json
from flask_restful import Resource
from . import people_file_path


def load_people_list():
    if os.path.exists(people_file_path):
        with open(people_file_path, "r") as f:
            return json.load(f)
    return []


def save_people_list(people_list: list):
    with open(people_file_path, "w") as f:
        json.dump(people_list, f)


class People(Resource):
    # @cross_origin(origins=["http://localhost:3000"])
    def get(self):
        return load_people_list()


class PeopleAction(Resource):
    # @cross_origin(origins=["http://localhost:3000"])
    def get(self, name):
        people_list = load_people_list()
        for x in people_list:
            if x["Data"] == name:
                return x
        return {"Data": None}

    # @cross_origin(origins=["http://localhost:3000"])
    def post(self, name):
        people_list = load_people_list()
        temp = {"Data": name}
        people_list.append(temp)
        save_people_list(people_list)
        return temp

    # @cross_origin(origins=["http://localhost:3000"])
    def delete(self, name):
        people_list = load_people_list()
        for ind, x in enumerate(people_list):
            if x["Data"] == name:
                people_list.pop(ind)
                save_people_list(people_list)
                return {"Note": "Deleted"}
