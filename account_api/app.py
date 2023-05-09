import os

from flask import Flask, request

from db import Base, engine
from resources.account import Account
from resources.ticket import Ticket

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


@app.route('/accounts', methods=['POST'])
def create_account():
    req_data = request.get_json()
    return Account.create(req_data)


@app.route('/accounts/<a_id>', methods=['GET'])
def get_account(a_id):
    return Account.get(a_id)


@app.route('/accounts/<a_id>', methods=['PUT'])
def update_account(a_id):
    # status = request.args.get('status')
    req_data = request.get_json()
    return Account.update(a_id, req_data)


@app.route('/accounts/<a_id>', methods=['DELETE'])
def delete_account(a_id):
    return Account.delete(a_id)


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
