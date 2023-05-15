import datetime
from flask import jsonify
from daos.ticket_dao import TicketDAO
from db import Session
import uuid


from datetime import datetime
from dateutil.relativedelta import relativedelta

class Ticket:
    @staticmethod
    def create(body):

        session = Session()
        ticket = TicketDAO(datetime.now(), datetime.now(), (datetime.now() + relativedelta(days=7)),
        "valid", body['price'], str(uuid.uuid4()), body['account_email'])
        session.add(ticket)
        session.commit()
        session.refresh(ticket)
        session.close()
        return jsonify({'ticket_id': ticket.id}), 200

    def update(body):
      pass

    # @staticmethod
    # def update(d_id, status):
    #     session = Session()
    #     delivery = session.query(DeliveryDAO).filter(DeliveryDAO.id == d_id)[0]
    #     delivery.status.status = status
    #     delivery.status.last_update = datetime.datetime.now()
    #     session.commit()
    #     return jsonify({'message': 'The delivery status was updated'}), 200
