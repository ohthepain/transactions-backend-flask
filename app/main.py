import uuid
import jsonpickle
from datetime import datetime
from flask import Flask, render_template, request
from flask_restx import Api, Resource, fields
from resource.ping import api as ping
from resource.transaction import api as transaction
from resource.account import api as accounts

print("Reticulating splines ...")

app = Flask(__name__)
api = Api(app, version="1.0", title="Transaction API", description="Transaction API for Alva Labs Test", doc="/swagger")
api.add_namespace(ping, "/")
api.add_namespace(transaction, "/")
api.add_namespace(accounts, "/")

if __name__ == '__main__':
    app.run(debug=True)

print("Transaction server is ready")
