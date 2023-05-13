from flask import make_response, jsonify

from daos.account_dao import AccountDAO
from db import Session
# see https://realpython.com/token-based-authentication-with-flask/
from jwtutil import encode_auth_token


class LoginAPI:
    @staticmethod
    def login(post_data):

        try:
            # fetch the user data
            session = Session()
            # check if user already exists
            user = session.query(AccountDAO).filter(AccountDAO.email_address == post_data.get('email_address')).first()
            session.close()
            if user:
                auth_token = encode_auth_token(user.id)
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token
                    }
                return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'There is no user.',
                }
            return make_response(jsonify(responseObject)), 404
        except Exception as e:
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500
