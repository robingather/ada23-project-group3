from datetime import datetime

from flask import jsonify

from constant import STATUS_CREATED
from daos.account_dao import AccountDAO
from daos.ticket_dao import TicketDAO
from db import Session


class Account:
    @staticmethod
    def create(body):
        session = Session()
        account = AccountDAO(body['first_name'], body['last_name'], body['email_address'],
          body['password'], body['user_type'], False, 0)
        session.add(account)
        session.commit()
        session.refresh(account)
        session.close()
        return jsonify({'account_id': account.id}), 200

    @staticmethod
    def get(d_id):
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        account = session.query(AccountDAO).filter(AccountDAO.id == d_id).first()

        if account:
            text_out = {
                "first_name:": account.first_name,
                "last_name:": account.last_name,
                "email_address:": account.email_address,
                "password:": account.password,
                "user_type:": account.user_type,
                "automatic_topup:": account.automatic_topup,
                "amount_topup:": account.amount_topup
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no account with id {d_id}'}), 404

    @staticmethod
    def update(a_id, body):
        session = Session()
        account = session.query(AccountDAO).filter(AccountDAO.id == d_id)[0]
        
        # delivery.status.status = status
        # delivery.status.last_update = datetime.datetime.now()
        session.commit()
        return jsonify({'message': 'The delivery status was updated'}), 200

    @staticmethod
    def delete(d_id):
        session = Session()
        effected_rows = session.query(AccountDAO).filter(AccountDAO.id == d_id).delete()
        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'There is no account with id {d_id}'}), 404
        else:
            return jsonify({'message': 'The account was removed'}), 200
