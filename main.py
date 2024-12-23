from flask import Flask
import os
import json
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
people_file = "people.json"


def load_people_list():
    if os.path.exists(people_file):
        with open(people_file, "r") as f:
            return json.load(f)
    return []


def save_people_list(people_list: list):
    with open(people_file, "w") as f:
        json.dump(people_list, f)


class People(Resource):
    def get(self):
        return load_people_list()


api.add_resource(People, "/Name/")


class PeopleAction(Resource):
    def get(self, name):
        people_list = load_people_list()
        for x in people_list:
            if x["Data"] == name:
                return x
        return {"Data": None}

    def post(self, name):
        people_list = load_people_list()
        temp = {"Data": name}
        people_list.append(temp)
        save_people_list(people_list)
        return temp

    def delete(self, name):
        people_list = load_people_list()
        for ind, x in enumerate(people_list):
            if x["Data"] == name:
                people_list.pop(ind)
                save_people_list(people_list)
                return {"Note": "Deleted"}


api.add_resource(PeopleAction, "/Name/<string:name>")

if __name__ == "__main__":
    app.run(debug=True)
