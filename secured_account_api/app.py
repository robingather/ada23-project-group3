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

@app.route('/verify', methods=['GET'])
def verify():
    # get the auth token
    auth_header = request.headers.get('Authorization')
    return Account.get(auth_header)

def check_if_authorize(req):
  auth_header = req.headers['Authorization']
  if 'AUTH_URL' in os.environ:
      auth_url = os.environ['AUTH_URL']
  else:
      auth_url = 'http://secure_api:5000/verify'
  result = requests.get(auth_url,
                          headers={'Content-Type': 'application/json',
                                  'Authorization': auth_header})
  # print("RES",result)
  # print("RES2",result.json())
  status_code = result.status_code
  print("status",status_code)
  try:
    data = result.json()['data'] if 'data' in result.json().keys() else None
    return status_code, data
  except Exception as e:
    return status_code, None

# Account end-points
# @app.route('/accounts/<a_id>', methods=['GET'])
# def get_account(a_id):
#     return Account.get(a_id)

# @app.route('/accounts/<a_id>', methods=['DELETE'])
# def delete_account(a_id):
#     return Account.delete(a_id)

# Ticket end-points
@app.route('/tickets', methods=['POST'])
def create_ticket():
  status_code, data = check_if_authorize(request)
  if status_code == 200:
    req_data = request.get_json()
    return Ticket.create(req_data, data)
  else:
    responseObject = {
        'status': 'fail',
        'message': 'Try again'
    }
    return make_response(jsonify(responseObject)), 401

@app.route('/ticketlist', methods=['GET'])
def get_tickets():
  status_code, data = check_if_authorize(request)
  if status_code == 200:
    # req_data = request.get_json()
    return Ticket.getAll(data)
  else:
    responseObject = {
        'status': 'fail',
        'message': 'Try again'
    }
    return make_response(jsonify(responseObject)), 401

# delete account
@app.route('/accounts',methods=['DELETE'])
def delete_account():
  status_code, data = check_if_authorize(request)
  if status_code == 200:
    return Account.delete(data)
  else:
    responseObject = {
        'status': 'fail',
        'message': 'Try again'
    }
    return make_response(jsonify(responseObject)), 401

# update account
@app.route('/accounts', methods=['PUT'])
def update_account():
  status_code, auth_data = check_if_authorize(request)
  if status_code == 200:
    req_data = request.get_json()
    return Account.update(req_data, auth_data)
  else:
    responseObject = {
        'status': 'fail',
        'message': 'Try again'
    }
    return make_response(jsonify(responseObject)), 401

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)


# TODO update ticket