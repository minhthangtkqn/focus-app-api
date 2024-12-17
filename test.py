from flask import Flask
from flask_restful import Resource, Api
import datetime
from flask import request
from functools import wraps

app = Flask(__name__)
api = Api(app)


def monitor(function=None):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print("Ip Address  : {} ".format(request.remote_user))
        _ = function(*args, **kwargs)
        print("Cookies : {} ".format(request.cookies))
        print(request.user_agent)
        return _

    return wrapper


def time(function=None):
    @wraps(function)
    # @monitor
    def wrapper(*args, **kwargs):
        s = datetime.datetime.now()
        _ = function(*args, **kwargs)
        e = datetime.datetime.now()
        print("Execution Time : {} ".format(e - s))
        return _

    return wrapper


def power_number(funct):
    def wrapped(*args, **kwargs):
        return funct() * funct()

    return wrapped


def double_number(funct):
    def wrapped(*args, **kwargs):
        return funct() * 2

    return wrapped


@double_number
@power_number
def return_number():
    return 10


class HelloWorld(Resource):
    # @time
    def get(self):
        print("Number: ", return_number())
        return {"hello": "world"}


api.add_resource(HelloWorld, "/wrap")

if __name__ == "__main__":
    app.run(debug=True)
