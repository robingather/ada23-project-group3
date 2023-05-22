from flask import jsonify, make_response

from daos.account_dao import AccountDAO
from db import Session
from jwtutil import encode_auth_token, decode_auth_token


# see https://realpython.com/token-based-authentication-with-flask/

class Account:

    @staticmethod
    def create(post_data):
        session = Session()
        # check if user already exists
        print("hello")
        user = session.query(AccountDAO).filter(AccountDAO.id == post_data.get('email_address')).first()
        if not user:
            try:
                user = AccountDAO(
                    first_name=post_data.get('first_name'),
                    last_name=post_data.get('last_name'),
                    user_type=post_data.get('user_type'),
                    automatic_topup= False,
                    amount_topup = 0,
                    email_address=post_data.get('email_address'),
                    password=post_data.get('password')
                )

                # insert the user
                session.add(user)
                session.commit()
                # generate the auth token
                auth_token = encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token
                }
                session.close()
                return make_response(jsonify(responseObject)), 200
            except Exception as e:
                print(e)
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202

    @staticmethod
    def get(auth_header):
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = decode_auth_token(auth_token)
            if not isinstance(resp, str):
                session = Session()
                # check if user already exists
                user = session.query(AccountDAO).filter(AccountDAO.id == resp).first()
                responseObject = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email_address': user.email_address,
                        'user_type':user.user_type,
                        'first_name':user.first_name,
                        'last_name':user.last_name
                    }
                }
                session.close()
                return make_response(jsonify(responseObject)), 200
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 401

    @staticmethod
    def delete(data):
      session = Session()
      user = session.query(AccountDAO).filter(AccountDAO.email_address == data.get('email_address')).delete()
      if(user):
        try:
          session.commit()
          responseObject = {
            'status': 'success',
            'message': 'deleted user with email %s' % data.get('email_address')
          }
          session.close()
          return make_response(jsonify(responseObject)), 200
        except Exception as e:
          print(e)
          responseObject = {
              'status': 'fail',
              'message': 'Some error occurred. Please try again.'
          }
          return make_response(jsonify(responseObject)), 401
      else:
        responseObject = {
            'status': 'fail',
            'message': ('account with %s doesn\'t exist.' % data.get('email_address'))
        }
        return make_response(jsonify(responseObject)), 401

    @staticmethod
    def update(req_data, auth_data):
        session = Session()
        account = session.query(AccountDAO).filter(AccountDAO.email_address == auth_data.get("email_address")).first()
        if(req_data.get("first_name")):
          account.first_name = req_data.get("first_name")
        if(req_data.get("last_name")):
          account.last_name = req_data.get("last_name")
        if(req_data.get("email_address")):
          account.email_address = req_data.get("email_address")
        if(req_data.get("user_type")):
          account.user_type = req_data.get("user_type")
        if(req_data.get("password")):
          account.password = req_data.get("password")
        session.commit()
        responseObject = {
            'status': 'success',
            'data': {
                'user_id': account.id,
                'email_address': account.email_address,
                'user_type':account.user_type,
                'first_name':account.first_name,
                'last_name':account.last_name
            }
        }
        return make_response(jsonify(responseObject)), 200
