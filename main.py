from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from service.gold_price import GoldPrice, GoldPriceActionWithoutId, GoldPriceList
from service.people import People, PeopleAction
from service.flash_card import (
    FlashCard,
    FlashCardActionWithId,
    FlashCardActionWithoutId,
)

app = Flask(__name__)
CORS(app, resources=r"/*")  # all origins
# CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})
# CORS(app, origins=["http://localhost:3000"])
# CORS(app, resources={r"/card/*": {"origins": ["http://localhost:3000"]}})
# CORS(app, resources={r"/name/*": {"origins": ["http://localhost:3000"]}})
api = Api(app)


api.add_resource(People, "/name/")
api.add_resource(PeopleAction, "/name/<string:name>")
api.add_resource(FlashCard, "/card/")
api.add_resource(FlashCardActionWithoutId, "/card:<string:command>/")
api.add_resource(FlashCardActionWithId, "/card/<string:id>")
api.add_resource(GoldPrice, "/gold-price/")
api.add_resource(GoldPriceList, "/gold-price-list/")
api.add_resource(GoldPriceActionWithoutId, "/gold-price:<string:command>/")

if __name__ == "__main__":
    app.run(debug=True)
