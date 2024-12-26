from flask import Flask
import os
import json
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
# CORS(app, resources=r"/*")
CORS(app)
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


@app.route("/name", methods=["GET"])
def get_people_list():
    return load_people_list()


@app.route("/name/<string:name>", methods=["GET"])
def get_person_by_name(name):
    people_list = load_people_list()
    for x in people_list:
        if x["Data"] == name:
            return x
    return {"Data": None}


@app.route("/name/<string:name>", methods=["POST"])
def add_person(name):
    people_list = load_people_list()
    temp = {"Data": name}
    people_list.append(temp)
    save_people_list(people_list)
    return temp


@app.route("/name/<string:name>", methods=["DELETE"])
def delete_person_by_name(name):
    people_list = load_people_list()
    for ind, x in enumerate(people_list):
        if x["Data"] == name:
            people_list.pop(ind)
            save_people_list(people_list)
            return {"Note": "Deleted"}


if __name__ == "__main__":
    app.run(debug=True)
