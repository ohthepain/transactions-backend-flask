import uuid
import jsonpickle
from datetime import datetime
from flask import Flask, render_template, request
from flask_restx import Api, Resource, fields
# from model.transaction import Transaction
from resource.ping import api as ping
from resource.transaction import api as transaction
from resource.account import api as accounts

app = Flask(__name__)
api = Api(app, version="1.0", title="Transaction API", description="Transaction API for Alva Labs Test", doc="/swagger")
api.add_namespace(ping, "/")
api.add_namespace(transaction, "/")
api.add_namespace(accounts, "/")

print("Some example guids ...\n566944be-2dab-460b-b3ed-eeeebd8c5618\ndd3d7604-73b9-4e06-a164-4f6192fe52df\nd80d61a0-b17c-4b9c-94dd-bc2a3428c9f9")

if __name__ == '__main__':
    app.run(debug=True)
