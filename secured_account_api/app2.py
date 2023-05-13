from flask import Flask, request
import os

from db import Base, engine
from resources.loginapi import LoginAPI
from resources.account2 import Account

app = Flask(__name__)
app.config["DEBUG"] = True

Base.metadata.create_all(engine)


@app.route('/register', methods=['POST'])
def register():
    req_data = request.get_json()
    return Account.create(req_data)


@app.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()
    return LoginAPI.login(req_data)


@app.route('/verify', methods=['POST'])
def verify():
    # get the auth token
    auth_header = request.headers.get('Authorization')
    return Account.get(auth_header)


# app.run(host='0.0.0.0', port=5000)
if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)