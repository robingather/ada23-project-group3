from flask import Flask, request, make_response, jsonify
import os
import requests
from db import Base, engine
from resources.loginapi import LoginAPI
from resources.account import Account
from resources.ticket import Ticket

app = Flask(__name__)
app.config["DEBUG"] = True

Base.metadata.create_all(engine)

# Authentication end-points
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

# Account end-points
@app.route('/accounts/<a_id>', methods=['GET'])
def get_account(a_id):
    return Account.get(a_id)

@app.route('/accounts/<a_id>', methods=['DELETE'])
def delete_account(a_id):
    return Account.delete(a_id)

# Ticket end-points
@app.route('/tickets', methods=['POST'])
def create_ticket():
  if check_if_authorize(request) == 200:
    req_data = request.get_json()
    return Ticket.create(req_data)
  else:
    responseObject = {
        'status': 'fail',
        'message': 'Try again'
    }
    return make_response(jsonify(responseObject)), 401

def check_if_authorize(req):
    auth_header = req.headers['Authorization']
    if 'AUTH_URL' in os.environ:
        auth_url = os.environ['AUTH_URL']
    else:
        auth_url = 'http://securedapi_ct:5000/verify'
    result = requests.post(auth_url,
                           headers={'Content-Type': 'application/json',
                                    'Authorization': auth_header})
    status_code = result.status_code
    print(status_code)
    print(result.json())
    return status_code

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)


# TODO auth tickets
# TODO get tickets