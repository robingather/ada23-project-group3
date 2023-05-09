import datetime
from flask import jsonify
from daos.account_dao import AccountDAO
from db import Session
import uuid


from datetime import datetime
from dateutil.relativedelta import relativedelta

class Ticket:
    @staticmethod
    def create(body):

        # new_time = (datetime.now() + relativedelta(days=5)).strftime('%d/%m/%Y %H:%M:%S')
        session = Session()
        ticket = TicketDAO(datetime.now(), datetime.now(), (datetime.now() + relativedelta(days=7)),
        "valid", body['price'], str(uuid.uuid4()), body['account_email'])
        session.add(ticket)
        session.commit()
        session.refresh(ticket)
        session.close()
        return jsonify({'ticket_id': ticket.id}), 200

    # @staticmethod
    # def update(d_id, status):
    #     session = Session()
    #     delivery = session.query(DeliveryDAO).filter(DeliveryDAO.id == d_id)[0]
    #     delivery.status.status = status
    #     delivery.status.last_update = datetime.datetime.now()
    #     session.commit()
    #     return jsonify({'message': 'The delivery status was updated'}), 200
