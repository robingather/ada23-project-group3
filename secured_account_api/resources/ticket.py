import datetime
from flask import jsonify, make_response
from daos.ticket_dao import TicketDAO
from db import Session
import uuid


from datetime import datetime
from dateutil.relativedelta import relativedelta

class Ticket:
    @staticmethod
    def create(body, auth):

        # new_time = (datetime.now() + relativedelta(days=5)).strftime('%d/%m/%Y %H:%M:%S')
        session = Session()
        ticket = TicketDAO(body['route_id'], datetime.now(), datetime.now(), (datetime.now() + relativedelta(days=7)),
        "valid", body['price'], str(uuid.uuid4()), auth['email_address'])
        session.add(ticket)
        session.commit()
        session.refresh(ticket)
        session.close()
        return jsonify({'ticket_id': ticket.id}), 200

    def getAll(body):
      session = Session()
      print(body, body['email_address'])
      tickets = session.query(TicketDAO).filter(TicketDAO.account_email == body['email_address'])
      if tickets:
        response = {}
        for ticket in tickets:
          response[ticket.id] = {
              "route_id:": ticket.route_id,
              "start_date" : ticket.start_date,
              "purchase_date" : ticket.purchase_date,
              "end_date" : ticket.end_date,
              "status" : ticket.status,
              "price" : ticket.price,
              "code" : ticket.code
          }
        session.close()
        return jsonify(response), 200
      else:
          session.close()
          return jsonify({'message': 'There are no tickets for account with email %s' % body['email_address']}), 404

    @staticmethod
    def delete(t_id, auth_data):
      session = Session()
      ticket = session.query(TicketDAO).filter(TicketDAO.id == t_id).delete()
      if(ticket):
        try:
          session.commit()
          responseObject = {
            'status': 'success',
            'message': 'deleted ticket with id %s for account %s' % (t_id, auth_data.get("email_address"))
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
            'message': ('ticket with id %s doesn\'t exist.' % t_id)
        }
        return make_response(jsonify(responseObject)), 401

    # @staticmethod
    # def update(d_id, status):
    #     session = Session()
    #     delivery = session.query(DeliveryDAO).filter(DeliveryDAO.id == d_id)[0]
    #     delivery.status.status = status
    #     delivery.status.last_update = datetime.datetime.now()
    #     session.commit()
    #     return jsonify({'message': 'The delivery status was updated'}), 200
